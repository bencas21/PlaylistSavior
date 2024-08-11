import os

class Config:
    SECRET_KEY = os.urandom(64)
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    REDIRECT_URI = 'https://flask-service.b2hrcq1s6o076.us-west-2.cs.amazonlightsail.com/callback'
    SCOPE = 'user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state'
    SESSION_TYPE = 'filesystem'
    OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')