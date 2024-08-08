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

def __track_id_to_title_and_artist__(track_id):
    track = sp.track(track_id)
    return f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"

def recomend_songs(json_string):
    track_ids = __recomendation_to_track_ids__(json_string)
    if not track_ids:
        return "No recommendations found."
    
    return "\n".join([__track_id_to_title_and_artist__(track_id) for track_id in track_ids])



