select
    station_id,
    latitude,
    longitude
from {{ ref('dim_station') }}
where latitude < -90
   or latitude > 90
   or longitude < -180
   or longitude > 180
