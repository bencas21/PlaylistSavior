from flask import Flask
from flask_session import Session
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from .config import Config
from .spotify import sp, sp_oauth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app)

    from . import routes
    app.register_blueprint(routes.bp)

    return app
