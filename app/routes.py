import logging
from flask import Blueprint, redirect, request, session, url_for, render_template, jsonify
from .spotify import sp, sp_oauth, cache_handler, recomend_songs, create_new_playlist, track_ids_to_tracks
from .ai_service import AIService

bp = Blueprint('main', __name__)

ai_service = AIService()

@bp.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return render_template('playlists.html', user_name=sp.current_user()['display_name'])

@bp.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('main.home'))

@bp.route('/get_recommendations', methods=['GET', 'POST'])
def get_recommendations():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    user_question = None
    chatbot_response = None

    if request.method == 'POST':
        user_question = request.form.get('user-input')  # Ensure this matches the input name in the form
        if user_question:
            try:
                # Get the initial chatbot response
                chatbot_response = ai_service.get_response_reccomendation(user_question)
            except Exception as e:
                logging.error(f"Error during chatbot invocation: {e}")
                output = "Sorry, an error occurred while processing your request."

        # Assuming `recomend_songs` formats or processes the chatbot response
        chatbot_response = recomend_songs(chatbot_response, user_question)
        session['tracks_for_playlist'] = []
        
        return render_template(
            'playlists.html', 
            user_question=user_question, 
            chatbot_response=chatbot_response,
            playlist_tracks=session.get('tracks_for_playlist', []),
            user_name=sp.current_user()['display_name']
        )

@bp.route('/add_to_playlist', methods=['PUT'])
def add_to_playlist():
    try:
        data = request.get_json()

        song_id = data.get('song_id')
     
        if 'tracks_for_playlist' not in session:
            session['tracks_for_playlist'] = []
        
        if song_id not in session['tracks_for_playlist']:
            session['tracks_for_playlist'].append(song_id)
    
        # Return updated tracks as JSON
        return jsonify({'success': True, 'tracks': track_ids_to_tracks(session.get('tracks_for_playlist', []))})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/add_spotify_playlist', methods=['POST'])
def add_spotify_playlist():
    try:
        create_new_playlist(sp.current_user()['id'], playlist_name="AI Generated Playlist", track_ids=session.get('tracks_for_playlist', []))
        return jsonify({'success': True})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/logout')
def logout():
    # Clear the session
    session.clear()
    
    # Redirect to the home page or login page
    return redirect(url_for('main.home'))

@bp.route('/play_music')
def play_music():
    
    return render_template('play_music.html')


@bp.route('/get_spotify_token')
def get_spotify_token():
    token = sp_oauth.get_access_token()["access_token"]
    return jsonify({'token': token})









