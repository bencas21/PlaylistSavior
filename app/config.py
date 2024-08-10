import os

class Config:
    SECRET_KEY = os.urandom(64)
    CLIENT_ID = '194ca0faa98d44e9b9b9940785c64e8d'
    CLIENT_SECRET = '253d7220dbc84f02ba9d53c75a0bf29d'
    REDIRECT_URI = 'http://localhost:5000/callback'
    SCOPE = 'user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private playlist-modify-public playlist-modify-private'
    SESSION_TYPE = 'filesystem'