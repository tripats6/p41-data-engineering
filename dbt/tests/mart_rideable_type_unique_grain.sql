select
    rideable_type,
    member_casual,
    count(*) as row_count
from {{ ref('mart_rideable_type') }}
group by
    rideable_type,
    member_casual
having count(*) > 1
