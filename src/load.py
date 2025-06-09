import os
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

def load_to_snowflake(records, table_name="spotify_tracks"):
    if not records:
        print("No records to load.")
        return

    df = pd.DataFrame(records)

    # Read Snowflake config
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    full_table_name = f"{database}.{schema}.{table_name}"
    temp_table = f"{database}.{schema}.{table_name}_staging"

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=database,
        schema=schema,
        role=os.getenv("SNOWFLAKE_ROLE"),
    )
    cs = conn.cursor()

    try:
        # Create table if it doesn't exist
        cs.execute(f"""
        CREATE TABLE IF NOT EXISTS {full_table_name} (
            track_id STRING,
            track_name STRING,
            track_uri STRING,
            track_href STRING,
            explicit BOOLEAN,
            duration_ms NUMBER,
            artist_id STRING,
            artist_name STRING,
            artist_uri STRING,
            album_id STRING,
            album_name STRING,
            album_release_date STRING,
            album_artwork_url STRING,
            played_at TIMESTAMP_TZ,
            context_type STRING,
            context_uri STRING
        )
        """)

        # Drop and create staging table
        cs.execute(f"DROP TABLE IF EXISTS {temp_table}")
        cs.execute(f"CREATE TEMP TABLE {temp_table} LIKE {full_table_name}")

        # Insert into staging
        insert_stmt = f"""
        INSERT INTO {temp_table} (
            track_id, track_name, track_uri, track_href, explicit, duration_ms,
            artist_id, artist_name, artist_uri,
            album_id, album_name, album_release_date, album_artwork_url,
            played_at, context_type, context_uri
        )
        VALUES (%(track_id)s, %(track_name)s, %(track_uri)s, %(track_href)s, %(explicit)s, %(duration_ms)s,
                %(artist_id)s, %(artist_name)s, %(artist_uri)s,
                %(album_id)s, %(album_name)s, %(album_release_date)s, %(album_artwork_url)s,
                %(played_at)s, %(context_type)s, %(context_uri)s)
        """
        for record in records:
            cs.execute(insert_stmt, record)

        # Merge from staging into main table to avoid duplicates
        merge_sql = f"""
        MERGE INTO {full_table_name} AS target
        USING {temp_table} AS source
        ON target.played_at = source.played_at
        WHEN NOT MATCHED THEN
            INSERT (
                track_id, track_name, track_uri, track_href, explicit, duration_ms,
                artist_id, artist_name, artist_uri,
                album_id, album_name, album_release_date, album_artwork_url,
                played_at, context_type, context_uri
            )
            VALUES (
                source.track_id, source.track_name, source.track_uri, source.track_href, source.explicit, source.duration_ms,
                source.artist_id, source.artist_name, source.artist_uri,
                source.album_id, source.album_name, source.album_release_date, source.album_artwork_url,
                source.played_at, source.context_type, source.context_uri
            )
        """
        cs.execute(merge_sql)

        print(f"Deduplicated and loaded {len(records)} records into {full_table_name}")
    finally:
        cs.close()
        conn.close()
