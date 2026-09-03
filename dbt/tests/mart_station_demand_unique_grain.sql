select
    station_id,
    station_name,
    member_casual,
    count(*) as row_count
from {{ ref('mart_station_demand') }}
group by
    station_id,
    station_name,
    member_casual
having count(*) > 1
