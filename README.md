# PlaylistSavior

A Flask app that turns a natural-language request ("upbeat 90s road trip songs") into a real Spotify playlist. An LLM interprets the request and generates track/artist recommendations, which are then created as a playlist through the Spotify Web API.

## How it works

1. The user describes the kind of playlist they want.
2. `ai_service.py` prompts an LLM (via LangChain/OpenAI) for song and artist recommendations matching the request.
3. `spotify.py` uses Spotipy to search Spotify and assemble the results into a new playlist on the user's account.

## Stack

Flask, Flask-Session, Spotipy (Spotify Web API), LangChain + OpenAI

## Setup

```bash
pip install -r requirements.txt
# set Spotify and OpenAI credentials — see app/config.py
python run.py
```
