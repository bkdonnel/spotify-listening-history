
with base as (

    select *
    from {{ ref('stg_spotify_tracks') }}

),

aggregated as (

    select
        track_id,
        track_name,
        artist_name,
        album_name,
        album_artwork_url,
        year,
        month,
        count(*) as play_count,
        sum(duration_minutes)::numeric(10,2) as total_play_time_minutes

    from base
    group by
        track_id, track_name, artist_name, album_name, album_artwork_url, year, month

)

select *
from aggregated
order by play_count desc
limit 5
