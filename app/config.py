import os

class Config:
    SECRET_KEY = os.urandom(64)
    CLIENT_ID = '02149e0430f84e3e851a9b2ae1781c70'
    CLIENT_SECRET = '1652589ce23a467b917ec62d01ee5c7d'
    REDIRECT_URI = 'http://localhost:5000/callback'
    SCOPE = 'user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private playlist-modify-public playlist-modify-private'
    SESSION_TYPE = 'filesystem'