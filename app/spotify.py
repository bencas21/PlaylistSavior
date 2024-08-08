import json
from flask import session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from .config import Config

# Setup Spotipy with Flask session cache handler
cache_handler = FlaskSessionCacheHandler(session)

sp_oauth = SpotifyOAuth(
    client_id=Config.CLIENT_ID,
    client_secret=Config.CLIENT_SECRET,
    redirect_uri=Config.REDIRECT_URI,
    scope=Config.SCOPE,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)

def __get_recommendations_from_json__(json_string):
    # Remove the 'json' tag but keep the rest of the string intact
    cleaned_json_string = json_string.replace('```json', '').replace('```', '').strip()
    
    # Parse the cleaned JSON string into a dictionary
    try:
        params = json.loads(cleaned_json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    
    # Convert artist names to IDs
    if params.get("seed_artists"):
        artist_names = params["seed_artists"]
        artist_ids = []
        for name in artist_names:
            artist_id = artist_name_to_id(name)
            if artist_id:
                artist_ids.append(artist_id)
            else:
                print(f"Artist '{name}' not found.")
        params["seed_artists"] = artist_ids
    
    if params.get("seed_tracks"):
        track_names = params["seed_tracks"]
        track_ids = []
        for name in track_names:
            track_id = song_name_to_id(name)
            if track_id:
                track_ids.append(track_id)
            else:
                print(f"Track '{name}' not found.")
        params["seed_tracks"] = track_ids

    # Prepare the params dictionary for the recommendations function
    recommendations_params = {
        "seed_artists": params.get("seed_artists"),
        "seed_genres": params.get("seed_genres", []),  # Ensure this is a list
        "seed_tracks": params.get("seed_tracks"),
        "limit": params.get("limit", 20),  # Default to 20 if not provided
        "market": params.get("market"),
        **{key: value for key, value in params.items() if key not in ["seed_artists", "seed_genres", "seed_tracks", "limit", "market"]}
    }

    # Ensure seed_genres is a list of strings
    if isinstance(recommendations_params["seed_genres"], str):
        recommendations_params["seed_genres"] = [recommendations_params["seed_genres"]]
    
    print(f"Recommendations params: {recommendations_params}")
    # Call the recommendations function
    try:
        return sp.recommendations(**recommendations_params)
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return None

    
def __recomendation_to_track_ids__(json_string):
    recommendations = __get_recommendations_from_json__(json_string)
    if recommendations and "tracks" in recommendations:
        return [track["id"] for track in recommendations["tracks"]]
    return []

def __track_ids_to_title_and_artist__(track_ids):
    tracks = sp.tracks(track_ids)["tracks"]
    return [
        f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
        for track in tracks
    ]


def recomend_songs(json_string):
    track_ids = __recomendation_to_track_ids__(json_string)
    if not track_ids:
        return "No recommendations found."
    
    return __track_ids_to_title_and_artist__(track_ids)

def get_genre_list():
    return sp.recommendation_genre_seeds()["genres"]

def artist_name_to_id(artist_name):
    results = sp.search(q=f"artist:{artist_name}", type="artist")
    if "artists" in results and "items" in results["artists"]:
        artists = results["artists"]["items"]
        if artists:
            return artists[0]["id"]
    return None


def song_name_to_id(song_name):
    results = sp.search(q=f"track:{song_name}", type="track", limit=1)
    if "tracks" in results and "items" in results["tracks"]:
        tracks = results["tracks"]["items"]
        if tracks:
            return tracks[0]["id"]
    return None






