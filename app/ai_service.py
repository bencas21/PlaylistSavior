import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
from .spotify import get_genre_list
from .get_reccomendation_prompt import get_reccomendation_prompt
from .config import Config


class AIService:
    def __init__(self):
        self.chatbot_pipeline = self.initialise_reccomendations_pipeline()

    def initialise_reccomendations_pipeline(self):
        try:
            prompt = ChatPromptTemplate.from_template(
                get_reccomendation_prompt()
            )

            model = ChatOpenAI(openai_api_key=Config.OPEN_API_KEY, model="gpt-4o-mini")
            format_output = StrOutputParser()

            chatbot_pipeline = prompt | model | format_output
            return chatbot_pipeline
        except Exception as e:
            logging.error(f"Failed to initialize chatbot: {e}")
            raise


    def get_response_reccomendation(self, UserRequest):
        try:
            response = self.chatbot_pipeline.invoke({
                'UserRequest': UserRequest,
                'genre_list': str(get_genre_list())
            })
            print("ai response reccomendation: ", response)
            return response
        except Exception as e:
            logging.error(f"Failed to get response: {e}")

