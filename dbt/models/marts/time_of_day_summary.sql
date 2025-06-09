
with base as (

    select *
    from {{ ref('stg_spotify_tracks') }}

),

aggregated as (

    select
        time_of_day,
        year,
        month,
        sum(duration_minutes)::numeric(10,2) as total_play_time_minutes,
        count(*) as play_count

    from base
    group by time_of_day, year, month

)

select *
from aggregated
order by
    year,
    month,
    case
        when time_of_day = 'morning' then 1
        when time_of_day = 'afternoon' then 2
        when time_of_day = 'evening' then 3
        when time_of_day = 'night' then 4
    end
