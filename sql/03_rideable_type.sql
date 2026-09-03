select
    rideable_type,
    member_casual,
    trip_count,
    avg_ride_duration_seconds,
    median_ride_duration_seconds
from analytics.mart_rideable_type
order by
    rideable_type,
    member_casual;
