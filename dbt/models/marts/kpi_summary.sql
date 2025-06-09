
with base as (

    select *
    from {{ ref('stg_spotify_tracks') }}

),

aggregated as (

    select
        year,
        month,
        count(*) as total_songs_played,
        round(sum(duration_minutes) / 60.0, 2) as total_play_time_hours,
        count(distinct album_id) as total_albums,
        count(distinct artist_id) as total_artists

    from base
    group by year, month

)

select *
from aggregated
order by year desc, month desc
