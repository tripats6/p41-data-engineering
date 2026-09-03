import pytest

from ingestion.ingest import TRIP_URL_TEMPLATE, validate_month


def test_trip_url_template():
    month = "202501"

    url = TRIP_URL_TEMPLATE.format(month=month)

    assert url == (
        "https://divvy-tripdata.s3.amazonaws.com/"
        "202501-divvy-tripdata.zip"
    )


def test_validate_month():
    validate_month("202501")

    with pytest.raises(ValueError):
        validate_month("202513")

    with pytest.raises(ValueError):
        validate_month("2025")
