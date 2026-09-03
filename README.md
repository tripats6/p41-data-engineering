Particle41 Data Engineering Challenge

Overview

This project implements an end-to-end data pipeline for Divvy bike-share data using Python, DuckDB, and dbt Core.

The pipeline ingests three consecutive months of Divvy trip data (January–March 2025) together with the current Divvy GBFS station information, models the data into a dimensional structure, applies data-quality tests, and produces analytical marts and SQL-based findings.

The design prioritizes correctness, reproducibility, explicit data-quality decisions, and a simple execution path.

Tech Stack

Python 3.11+

DuckDB 1.5.5

dbt Core 1.12.3

dbt-duckdb 1.11.0

pytest 8.4.2

Setup

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install the pinned dependencies:

pip install -r requirements.txt

Running the Pipeline

The ingestion entrypoint accepts one or more months in YYYYMM format.

For the challenge dataset:

python -m ingestion.ingest --months 202501 202502 202503

Then run dbt:

dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt

The Makefile provides the intended single-command workflow:

make pipeline

The pipeline is designed to stop when an earlier stage fails.

Ingestion

The Python ingestion process:

Downloads the selected monthly Divvy trip ZIP files.

Downloads the current GBFS station information.

Caches downloaded files locally.

Loads trip data into raw.trips.

Loads station data into raw.stations.

Rebuilds the selected trip dataset on each run, making repeated runs idempotent.

Preserves source trip columns and performs cleaning downstream in dbt.

The ingestion entrypoint allows the caller to restrict the months being processed.

Data Model

Raw Layer

raw.trips

One row per source trip record.

raw.stations

Current Divvy GBFS station information.

Staging Layer

stg_trips

Staging view of the selected trip data. Grain: one row per trip.

stg_stations

Staging view of the current GBFS station data. Grain: one row per station.

Dimensions

dim_station

Current station dimension. Grain: one row per station.

dim_date

Calendar dimension derived from the dates represented in the trip data. Grain: one row per calendar date.

Fact

fct_trips

Trip-level fact table. Grain: one row per ride.

The fact contains the trip identifier, timestamps, rider type, bike type, historical station information, coordinates, and calculated ride duration.

Analytical Marts

mart_station_demand

Grain: one row per historical starting station ID, historical station name, and rider type.

Used to analyze station demand by member vs. casual riders.

mart_usage_patterns

Grain: one row per hour, day of week, and rider type.

Used to analyze when members and casual riders use the system.

mart_rideable_type

Grain: one row per rideable type and rider type.

Used to compare bike-type usage and ride duration.

Key Modeling Decisions

Station IDs

The current GBFS station IDs do not directly overlap with the historical trip station IDs in the supplied data.

Because of this, the trip fact does not enforce a station foreign-key relationship to the current GBFS station dimension. Doing so would incorrectly classify valid historical station identifiers as referential-integrity failures.

The current GBFS station dataset is therefore treated as a current station reference rather than a historical lookup for the trip period.

Historical Station Names

Historical station names are retained from the trip data.

The same station ID can appear with different historical names, including names containing a trailing *. Rather than silently normalizing these values and potentially changing the historical data, the station-demand mart preserves the recorded station name.

Missing Station IDs

Trips without a start or end station ID are retained with null station identifiers.

They are not assigned to a station using an inferred or approximate mapping.

Ride Duration

Ride duration is calculated downstream from the trip start and end timestamps in the fact model.

Data-quality tests check that trips do not have negative durations or an end timestamp earlier than the start timestamp.

Data Quality

The dbt project includes:

unique and not_null tests on relevant keys.

Accepted-value tests for rider type and bike type.

A relationship test between trip start dates and dim_date.

Negative ride-duration validation.

Timestamp-order validation.

Station coordinate range validation.

Composite-grain uniqueness tests for the analytical marts.

The ingestion layer also contains pure Python unit tests for URL construction and month validation.

Reproducibility and Idempotency

Source downloads are cached locally.

Running ingestion multiple times for the same set of months rebuilds the selected raw trip dataset rather than appending duplicate records.

Generated source files, the DuckDB database, dbt build artifacts, and the Python virtual environment are excluded from version control.

The project is intended to be runnable from a fresh clone using the documented setup and pipeline commands.

Analytics

Three analytical SQL queries are provided:

sql/01_station_demand.sql — station demand by rider type.

sql/02_usage_patterns.sql — usage patterns by hour, day of week, and rider type.

sql/03_rideable_type.sql — bike type usage and ride-duration comparison.

The resulting findings are documented in findings.md.

Findings

The analysis shows that:

Members account for substantially more trips than casual riders.

Demand is concentrated among a relatively small group of high-volume starting stations.

Casual riders generally have longer rides than members.

Electric bikes account for the majority of trips for both rider types.

Station identifiers and names require care because historical trip data and the current GBFS snapshot are not directly interchangeable.

Detailed results and supporting numbers are available in findings.md.

AI Usage

AI assistance used during development is documented in AI_USAGE.md, including the areas where AI contributed and the engineering decisions that were reviewed and validated manually.

If More Time Were Available

Potential improvements would include:

Developing a more robust historical station reconciliation strategy.


Adding incremental ingestion for larger historical periods.

Adding station-to-station flow analysis.

Adding CI to execute the complete pipeline and test suite automatically.

Performing a fresh-clone validation on a separate machine before submission.