# app/routes.py

import logging
from flask import Blueprint, redirect, request, session, url_for, render_template
from .spotify import sp, sp_oauth, cache_handler, recomend_songs
from .ai_service import AIService


bp = Blueprint('main', __name__)

ai_service = AIService()

@bp.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return render_template('playlists.html')

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
    artist_only = False

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
        chatbot_response = recomend_songs(chatbot_response)
        
        return render_template(
            'playlists.html', 
            user_question=user_question, 
            chatbot_response=chatbot_response,
        )



