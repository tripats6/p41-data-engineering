select
    station_id,
    station_name,
    member_casual,
    trip_count
from analytics.mart_station_demand
order by
    trip_count desc;
