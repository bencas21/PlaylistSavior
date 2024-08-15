import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
from .spotify import get_genre_list
from .get_response_artist_only_prompt import get_response_artist_only_prompt
from .get_reccomendation_prompt import get_reccomendation_prompt
from .config import Config


class AIService:
    def __init__(self):
        self.chatbot_pipeline = self.initialise_reccomendations_pipeline()
        self.artist_only_pipeline = self.initialise_artist_only_pipeline()

    def initialise_reccomendations_pipeline(self):
        try:
            prompt = ChatPromptTemplate.from_template(
                get_reccomendation_prompt()
            )

            model = ChatOpenAI(openai_api_key=Config.OPEN_API_KEY, model="gpt-4o-mini", temperature=0.3)
            format_output = StrOutputParser()

            chatbot_pipeline = prompt | model | format_output
            return chatbot_pipeline
        except Exception as e:
            logging.error(f"Failed to initialize chatbot: {e}")
            raise

    def initialise_artist_only_pipeline(self):
        try:
            prompt = ChatPromptTemplate.from_template(
                get_response_artist_only_prompt()
            )

            model = ChatOpenAI(openai_api_key=Config.OPEN_API_KEY, model_name="gpt-4o-mini", temperature=0.3)
            format_output = StrOutputParser()

            artist_only_pipeline = prompt | model | format_output
            return artist_only_pipeline
        except Exception as e:
            logging.error(f"Failed to initialize artist-only pipeline: {e}")
            raise

    def get_response_reccomendation(self, UserRequest):
        try:
            response = self.chatbot_pipeline.invoke({
                'UserRequest': UserRequest,
                'genre_list': str(get_genre_list())
            })
            artist_only_str = self.get_response_artist_only(UserRequest)
                
            # Convert the string response to a boolean
            artist_only = artist_only_str.strip().lower() == "true"
                
            # Add artist_only to the initial chatbot response
            if isinstance(response, dict):
                response['artist_only'] = artist_only
            else:
                response = {
                    'response': response,
                    'artist_only': artist_only
                }
            response = self.process_ai_response(response)
            print("ai response reccomendation: ", response)
            return response
        except Exception as e:
            logging.error(f"Failed to get response: {e}")
            raise

    def get_response_artist_only(self, UserRequest):
        try:
            response = self.artist_only_pipeline.invoke({
                'UserRequest': UserRequest
            })
            return response
        except Exception as e:
            logging.error(f"Failed to get response: {e}")
            raise

    def process_ai_response(self, ai_response):
        try:
            # Extract the response string
            response_str = ai_response.get('response', '{}')

            # Parse the JSON string into a Python dictionary
            response_data = json.loads(response_str)

            # Add the 'artist_only' boolean to the response data
            response_data['artist_only'] = ai_response.get('artist_only', False)

            return response_data

        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            return None
