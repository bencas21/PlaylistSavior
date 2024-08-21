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

def __get_recommendations_from_json__(json_dict,user_request):
    
    
    # Parse the cleaned JSON string into a dictionary
    try:
        params = json_dict
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    
    # Convert artist names to IDs
    if "seed_artists" in params:
        artist_names = params["seed_artists"]
        artist_ids = []
        for name in artist_names:
            artist_id = artist_name_to_id(name)
            if artist_id:
                artist_ids.append(artist_id)
            else:
                print(f"Artist '{name}' not found.")
        params["seed_artists"] = artist_ids
    
    # Convert track names to IDs
    if "seed_tracks" in params:
        track_names = params["seed_tracks"]
        track_ids = []
        for name in track_names:
            track_id = song_name_to_id(name)
            if track_id:
                track_ids.append(track_id)
            else:
                print(f"Track '{name}' not found.")
        params["seed_tracks"] = track_ids

    # Ensure all seed parameters are lists
    recommendations_params = {
        "seed_artists": params.get("seed_artists", []),  # Default to empty list if not provided
        "seed_genres": params.get("seed_genres", []),    # Ensure this is a list
        "seed_tracks": params.get("seed_tracks", []),    # Default to empty list if not provided
        "limit": params.get("limit", 20),                # Default to 20 if not provided
        **{key: value for key, value in params.items() if key not in ["seed_artists", "seed_genres", "seed_tracks", "limit","artist_only"]}
    }

    print(f"Recommendations params: {recommendations_params}")
    # Call the recommendations function
    try:
        if params["artist_only"] == True:
            return __recommendation_filter_single_artist__(sp.recommendations(**recommendations_params), recommendations_params["seed_artists"], user_request, recommendations_params["limit"])
        return sp.recommendations(**recommendations_params)
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return None

def __recomendation_to_track_ids__(json_string,user_request):
    recommendations = __get_recommendations_from_json__(json_string,user_request)

    if recommendations and "tracks" in recommendations:
        return [track["id"] for track in recommendations["tracks"]]
    return []

def track_ids_to_tracks(track_ids):
    tracks = sp.tracks(track_ids)["tracks"]
    return tracks

def recomend_songs(json_string, user_request):
    track_ids = __recomendation_to_track_ids__(json_string,user_request)
    if not track_ids:
        return "No recommendations found."
    
    return track_ids_to_tracks(track_ids)

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

def get_artist_from_track_id(track_id):
    track = sp.track(track_id)
    if "artists" in track and track["artists"]:
        return track["artists"][0]["name"]
    return None

def get_artist_ids_from_name(artist_name, num_artists):
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=num_artists)
    if "artists" in results and "items" in results["artists"]:
        artists = results["artists"]["items"]
        if artists:
            return [artist["id"] for artist in artists]
    return None

def get_artists_from_ids(artist_ids):
    return sp.artists(artist_ids)["artists"]

def get_artists_from_name(artist_name, num_artists):
    artist_ids = get_artist_ids_from_name(artist_name, num_artists)
    if artist_ids:
        return get_artists_from_ids(artist_ids)
    return None



def __recommendation_filter_single_artist__(recommendations, artist_ids, human_request, limit=10):
    # Initialize lists and sets to store filtered tracks and track IDs
    filtered_recommendations = []
    unique_track_ids = set()
    # Filter tracks from the initial recommendations
    if "tracks" in recommendations:
        for track in recommendations["tracks"]:
            # Check if any artist ID in the track matches any artist ID in artist_ids
            if any(artist['id'] in artist_ids for artist in track.get('artists', [])):
                if track['id'] not in unique_track_ids:
                    filtered_recommendations.append(track)
                    unique_track_ids.add(track['id'])
                    if len(filtered_recommendations) >= limit:
                        break

    # If not enough tracks, search for more
    if len(filtered_recommendations) < limit:
        # Perform search using the human request
        search_results = sp.search(q=human_request, type='track', limit=50)
        tracks = search_results.get('tracks', {}).get('items', [])

        # Filter these search results by artist name
        for track in tracks:
            if any(artist['id'] in artist_ids for artist in track.get('artists', [])):
                if track['id'] not in unique_track_ids:
                    filtered_recommendations.append(track)
                    unique_track_ids.add(track['id'])
                    if len(filtered_recommendations) >= limit:
                        break

        # Fetch more tracks if needed
        offset = 50
        while len(filtered_recommendations) < limit:
            more_results = sp.search(q=human_request, type='track', limit=50, offset=offset)
            more_tracks = more_results.get('tracks', {}).get('items', [])

            if not more_tracks:
                break

            for track in more_tracks:
                if any(artist['id'] in artist_ids for artist in track.get('artists', [])):
                    if track['id'] not in unique_track_ids:
                        filtered_recommendations.append(track)
                        unique_track_ids.add(track['id'])
                        if len(filtered_recommendations) >= limit:
                            break
            offset += 50

        # If still not enough tracks, get general recommendations without artist constraint
        if len(filtered_recommendations) < limit:
            remaining_limit = limit - len(filtered_recommendations)
            general_recommendations = sp.recommendations(seed_artists=artist_ids, limit=remaining_limit)
            for track in general_recommendations.get('tracks', []):
                if track['id'] not in unique_track_ids:
                    filtered_recommendations.append(track)
                    unique_track_ids.add(track['id'])
                    if len(filtered_recommendations) >= limit:
                        break

    # Return the required number of tracks
    return {"tracks": filtered_recommendations[:limit]}


def create_new_playlist(user_id, playlist_name, track_ids):
    playlist = sp.user_playlist_create(user_id, playlist_name)

    sp.playlist_add_items(playlist["id"], track_ids )
    playlist_id = playlist["id"]
    return playlist_id









