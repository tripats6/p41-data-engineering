select
    rideable_type,
    member_casual,
    count(*) as trip_count,
    avg(ride_duration_seconds) as avg_ride_duration_seconds,
    median(ride_duration_seconds) as median_ride_duration_seconds
from {{ ref('fct_trips') }}
group by
    rideable_type,
    member_casual