import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-read-recently-played"

def get_spotify_client():
    """Handles authentication and token refreshing with caching."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=os.path.join(os.getcwd(), ".cache")
    ))

def fetch_recent_tracks():
    """Fetch recently played tracks with full details including genres."""
    sp = get_spotify_client()
    results = sp.current_user_recently_played(limit=50)

    tracks = []
    for item in results["items"]:
        track = item["track"]
        album = track["album"]
        artist_id = track["artists"][0]["id"]
        artist_info = sp.artist(artist_id)
        genres = artist_info.get("genres", [])

        tracks.append({
            "track_id": track["id"],
            "track_name": track["name"],
            "track_uri": track["uri"],
            "track_href": track["href"],
            "explicit": track["explicit"],
            "duration_ms":track["duration_ms"],
            "artist_id": artist_id,
            "artist_name": artist_info.get("name"),
            "artist_uri": artist_info.get("uri"),
            "album_id": album["id"],
            "album_name": album["name"],
            "album_release_date": album["release_date"],
            "album_artwork_url": album["images"][0]["url"] if album["images"] else None,
            "played_at": item["played_at"],
            "context_type": item["context"]["type"] if item["context"] else None,
            "context_uri": item["context"]["uri"] if item["context"] else None
        })
    
    return tracks

if __name__ == "__main__":
    print(json.dumps(fetch_recent_tracks(), indent=4))
