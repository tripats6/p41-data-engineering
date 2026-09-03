with date_range as (

    select
        min(cast(started_at as date)) as min_date,
        max(cast(started_at as date)) as max_date
    from {{ ref('stg_trips') }}

),

dates as (

    select
        unnest(
            generate_series(
                min_date,
                max_date,
                interval '1 day'
            )
        )::date as date_day
    from date_range

)

select
    date_day,
    year(date_day) as year,
    month(date_day) as month,
    monthname(date_day) as month_name,
    day(date_day) as day_of_month,
    dayofweek(date_day) as day_of_week,
    dayname(date_day) as day_name,
    week(date_day) as week_of_year,
    quarter(date_day) as quarter
from dates