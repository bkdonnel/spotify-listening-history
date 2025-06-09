-- dbt/models/marts/artist_top_plays.sql

with base as (

    select *
    from {{ ref('stg_spotify_tracks') }}

),

aggregated as (

    select
        artist_id,
        artist_name,
        min(album_artwork_url) as album_artwork_url,  
        year,
        month,

        count(*) as song_play_count,
        count(distinct track_name) as unique_songs,
        sum(duration_minutes)::numeric(10,2) as total_play_time_minutes

    from base
    group by artist_id, artist_name, year, month

)

select *
from aggregated
order by song_play_count desc
limit 5
