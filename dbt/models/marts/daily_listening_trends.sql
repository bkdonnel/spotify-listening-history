
with base as (

    select *
    from {{ ref('stg_spotify_tracks') }}

),

daily as (

    select
        played_at::date as play_date,
        date_part('year', played_at) as year,
        date_part('month', played_at) as month,
        date_part('week', played_at) as week,
        date_part('dow', played_at) as day_of_week,
        count(*) as play_count,
        round(sum(duration_minutes), 2) as total_play_time_minutes

    from base
    group by 1, 2, 3, 4, 5

)

select *
from daily
order by play_date
