select
    station_id,
    station_name,
    short_name,
    longitude,
    latitude,
    capacity,
    has_kiosk,
    station_type,
    external_id,
    address
from {{ ref('stg_stations') }}