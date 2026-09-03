with trips as (

    select
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        start_station_name,
        start_station_id,
        end_station_name,
        end_station_id,
        start_lat,
        start_lng,
        end_lat,
        end_lng,
        member_casual
    from {{ ref('stg_trips') }}

)

select
    trips.ride_id,
    trips.rideable_type,

    cast(trips.started_at as date) as start_date,
    trips.started_at,
    trips.ended_at,

    trips.start_station_id,
    trips.start_station_name,
    trips.end_station_id,
    trips.end_station_name,

    trips.start_lat,
    trips.start_lng,
    trips.end_lat,
    trips.end_lng,

    trips.member_casual,

    datediff('second', trips.started_at, trips.ended_at) as ride_duration_seconds

from trips