select
    ride_hour,
    day_of_week,
    day_name,
    member_casual,
    trip_count,
    avg_ride_duration_seconds
from analytics.mart_usage_patterns
order by
    day_of_week,
    ride_hour,
    member_casual;
