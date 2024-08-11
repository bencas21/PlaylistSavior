import os

class Config:
    SECRET_KEY = os.urandom(64)
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    REDIRECT_URI = 'http://localhost:5000/callback'
    SCOPE = 'user-read-private user-read-email streaming playlist-read-private playlist-modify-private playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state user-read-currently-playing '
    SESSION_TYPE = 'filesystem'
    OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')