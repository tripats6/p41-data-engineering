select
    extract(hour from started_at) as ride_hour,
    dayofweek(started_at) as day_of_week,
    dayname(started_at) as day_name,
    member_casual,
    count(*) as trip_count,
    avg(ride_duration_seconds) as avg_ride_duration_seconds
from {{ ref('fct_trips') }}
where started_at is not null
group by
    extract(hour from started_at),
    dayofweek(started_at),
    dayname(started_at),
    member_casual