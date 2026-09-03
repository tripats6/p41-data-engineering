select
    ride_id,
    started_at,
    ended_at,
    ride_duration_seconds
from {{ ref('fct_trips') }}
where ride_duration_seconds < 0
