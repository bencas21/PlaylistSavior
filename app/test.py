import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests


# Setup Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='194ca0faa98d44e9b9b9940785c64e8d',
    client_secret='253d7220dbc84f02ba9d53c75a0bf29d',
    redirect_uri='http://localhost:5000/callback',
    scope='user-library-read playlist-read-private user-read-playback-state user-read-currently-playing'
))

def test_spotify_connection():
    try:
        print (sp.recommendation_genre_seeds())
        # Fetch the current user's details
        user = sp.current_user()
        print(f"User: {user['display_name']}")

        # Fetch user's playlists
        playlists = sp.current_user_playlists()
        print("\nUser's Playlists:")
        for playlist in playlists['items']:
            print(f"- {playlist['name']}")

        # Fetch tracks from the first playlist
        if playlists['items']:
            first_playlist_id = playlists['items'][0]['id']
            tracks = sp.playlist_tracks(first_playlist_id)
            print(f"\nTracks in the playlist '{playlists['items'][0]['name']}':")
            for track in tracks['items']:
                track_name = track['track']['name']
                artist_names = ", ".join(artist['name'] for artist in track['track']['artists'])
                print(f"- {track_name} by {artist_names}")

        # Fetch recommendations based on a genre
        recommendations = sp.recommendations(seed_genres=['pop'], limit=5)
        print("\nRecommendations:")
        for track in recommendations['tracks']:
            track_name = track['name']
            artist_names = ", ".join(artist['name'] for artist in track['artists'])
            print(f"- {track_name} by {artist_names}")

    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    test_spotify_connection()
