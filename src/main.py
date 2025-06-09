from extract import fetch_recent_tracks
from load import load_to_snowflake

def main():
    records = fetch_recent_tracks()
    load_to_snowflake(records)

if __name__ == "__main__":
    main()
