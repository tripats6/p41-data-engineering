select
    ride_id,
    started_at,
    ended_at
from {{ ref('fct_trips') }}
where ended_at < started_at
