

with base as (

    select *
    from {{ ref('stg_spotify_tracks') }}

),

weekly as (

    select
        date_trunc('week', played_at)::date as play_week,
        date_part('year', played_at) as year,
        date_part('week', played_at) as week,
        count(*) as play_count,
        round(sum(duration_minutes), 2) as total_play_time_minutes

    from base
    group by 1, 2, 3

)

select *
from weekly
order by play_week
