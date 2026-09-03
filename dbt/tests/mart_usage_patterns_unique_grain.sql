select
    ride_hour,
    day_of_week,
    member_casual,
    count(*) as row_count
from {{ ref('mart_usage_patterns') }}
group by
    ride_hour,
    day_of_week,
    member_casual
having count(*) > 1
