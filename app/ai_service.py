from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
from .get_reccomendation_prompt import get_reccomendation_prompt

class AIService:
    def __init__(self):
        self.chatbot_pipeline = self.initialise_llama3()

    def initialise_llama3(self):
        try:
            prompt = ChatPromptTemplate.from_template(
                get_reccomendation_prompt()
            )

            llama_model = Ollama(model="gemma2:2b")
            format_output = StrOutputParser()

            chatbot_pipeline = prompt | llama_model | format_output
            return chatbot_pipeline
        except Exception as e:
            logging.error(f"Failed to initialize chatbot: {e}")
            raise

    def get_response(self, UserRequest):
        try:
            response = self.chatbot_pipeline.invoke({'UserRequest': UserRequest})
            print("ai response: ", response)
            return response
        except Exception as e:
            logging.error(f"Failed to get response: {e}")
            raise
    

