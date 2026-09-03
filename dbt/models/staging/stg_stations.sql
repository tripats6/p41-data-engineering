select
    station_id,
    name as station_name,
    short_name,
    lon as longitude,
    lat as latitude,
    capacity,
    has_kiosk,
    station_type,
    external_id,
    address
from raw.stations