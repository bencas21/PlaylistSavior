from flask import session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from .config import Config

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
