from pathlib import Path
import argparse
import zipfile
import json

import duckdb
import requests


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DUCKDB_DIR = PROJECT_ROOT / "duckdb"

DB_PATH = DUCKDB_DIR / "divvy.duckdb"

TRIP_URL_TEMPLATE = (
    "https://divvy-tripdata.s3.amazonaws.com/"
    "{month}-divvy-tripdata.zip"
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ingest Divvy trip and station data into DuckDB."
    )

    parser.add_argument(
        "--months",
        nargs="+",
        required=True,
        help="Months to ingest in YYYYMM format, e.g. 202501 202502 202503.",
    )

    return parser.parse_args()


def validate_month(month: str) -> None:
    if len(month) != 6 or not month.isdigit():
        raise ValueError(
            f"Invalid month '{month}'. Expected format YYYYMM."
        )

    year = int(month[:4])
    month_number = int(month[4:])

    if year < 2000 or month_number < 1 or month_number > 12:
        raise ValueError(
            f"Invalid month '{month}'. Expected a valid YYYYMM date."
        )


def download_trip_data(month: str) -> Path:
    filename = f"{month}-divvy-tripdata.zip"
    destination = DATA_DIR / filename

    if destination.exists():
        print(f"Using cached file: {filename}")
        return destination

    url = TRIP_URL_TEMPLATE.format(month=month)

    print(f"Downloading: {url}")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    destination.write_bytes(response.content)

    print(f"Saved: {destination}")

    return destination

STATION_URL = (
    "https://gbfs.divvybikes.com/gbfs/en/station_information.json"
)


def download_station_data() -> Path:
    station_path = DATA_DIR / "station_information.json"

    if station_path.exists():
        print(f"Using cached file: {station_path.name}")
        return station_path

    print("Downloading station information...")
    response = requests.get(STATION_URL, timeout=60)
    response.raise_for_status()

    station_path.write_bytes(response.content)
    print(f"Downloaded: {station_path}")

    return station_path


def load_station_data(con, station_path: Path) -> None:
    with open(station_path, "r", encoding="utf-8") as file:
        payload = json.load(file)

    stations = payload["data"]["stations"]

    con.execute("DROP TABLE IF EXISTS raw.stations")

    con.execute(
        """
        CREATE TABLE raw.stations AS
        SELECT *
        FROM read_json_auto(?)
        """,
        [str(station_path)],
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE raw.stations AS
        SELECT
            station.*,
            last_updated,
            ttl,
            version
        FROM raw.stations,
        UNNEST(data.stations) AS t(station)
        """
    )

    print(f"Loaded {len(stations):,} stations into raw.stations")

def load_trip_data(con, zip_path: Path, first_file: bool = False) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        csv_files = [
            name
            for name in archive.namelist()
            if name.lower().endswith(".csv")
            and not name.startswith("__MACOSX/")
        ]

        if len(csv_files) != 1:
            raise ValueError(
                f"Expected exactly one CSV in {zip_path.name}, "
                f"found {len(csv_files)}."
            )

        csv_name = csv_files[0]

        print(f"Loading {csv_name} from {zip_path.name}")

        archive.extract(csv_name, DATA_DIR)

        csv_path = DATA_DIR / csv_name

        try:
            if first_file:
                con.execute(
                    """
                    CREATE OR REPLACE TABLE raw.trips AS
                    SELECT *
                    FROM read_csv_auto(?)
                    """,
                    [str(csv_path)],
                )
            else:
                con.execute(
                    """
                    INSERT INTO raw.trips
                    SELECT *
                    FROM read_csv_auto(?)
                    """,
                    [str(csv_path)],
                )

        finally:
            csv_path.unlink(missing_ok=True)


def main():
    args = parse_args()

    for month in args.months:
        validate_month(month)

    DATA_DIR.mkdir(exist_ok=True)
    DUCKDB_DIR.mkdir(exist_ok=True)

    print(f"Months selected: {args.months}")
    print(f"Data directory: {DATA_DIR}")
    print(f"DuckDB database: {DB_PATH}")

    zip_paths = []

    for month in args.months:
        zip_path = download_trip_data(month)
        zip_paths.append(zip_path)

    station_path = download_station_data()

    con = duckdb.connect(str(DB_PATH))

    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        con.execute("DROP TABLE IF EXISTS raw.trips")

        for index, zip_path in enumerate(zip_paths):
            load_trip_data(
                con,
                zip_path,
                first_file=(index == 0),
            )

        load_station_data(con, station_path)

        trip_count = con.execute(
            "SELECT COUNT(*) FROM raw.trips"
        ).fetchone()[0]

        print(f"Loaded {trip_count:,} trips into raw.trips")

    finally:
        con.close()


if __name__ == "__main__":
    main()