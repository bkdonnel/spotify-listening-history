-- dbt/models/staging/stg_spotify_tracks.sql

with source as (

    select
        *,
        row_number() over (partition by played_at order by played_at) as row_num
    from {{ source('spotify', 'spotify_tracks') }}

),

deduplicated as (

    select *
    from source
    where row_num = 1

),

transformed as (

    select
        played_at::timestamp as played_at,
        date_trunc('day', played_at::timestamp) as played_date,
        extract(month from played_at::timestamp) as month,
        extract(year from played_at::timestamp) as year,
        extract(hour from played_at::timestamp) as hour,

        -- Assign time of day buckets
        case 
            when extract(hour from played_at) between 5 and 11 then 'morning'
            when extract(hour from played_at) between 12 and 16 then 'afternoon'
            when extract(hour from played_at) between 17 and 20 then 'evening'
            else 'night'
        end as time_of_day,

        track_id,
        track_name,
        track_uri,
        track_href,
        explicit,
        duration_ms,
        (duration_ms / 60000.0)::float as duration_minutes, 

        artist_id,
        artist_name,
        artist_uri,

        album_id,
        album_name,
        album_release_date::date as album_release_date,
        album_artwork_url,

        context_type,
        context_uri

    from deduplicated

)

select * from transformed
