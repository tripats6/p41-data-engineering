select
    start_station_id as station_id,
    start_station_name as station_name,
    member_casual,
    count(*) as trip_count
from {{ ref('fct_trips') }}
where start_station_id is not null
group by
    start_station_id,
    start_station_name,
    member_casual