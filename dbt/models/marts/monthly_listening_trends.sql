
with base as (

    select *
    from {{ ref('stg_spotify_tracks') }}

),

monthly as (

    select
        date_trunc('month', played_at)::date as play_month,
        date_part('year', played_at) as year,
        date_part('month', played_at) as month,
        count(*) as play_count,
        round(sum(duration_minutes), 2) as total_play_time_minutes

    from base
    group by 1, 2, 3

)

select *
from monthly
order by play_month
