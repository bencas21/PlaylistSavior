from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
from get_reccomendation_prompt import get_reccomendation_prompt

class AIService:
    def __init__(self):
        self.chatbot_pipeline = self.initialise_llama3()

    def initialise_llama3(self):
        try:
            prompt = ChatPromptTemplate.from_template(
                get_reccomendation_prompt()
            )

            llama_model = Ollama(model="llama3.1")
            format_output = StrOutputParser()

            chatbot_pipeline = prompt | llama_model | format_output
            return chatbot_pipeline
        except Exception as e:
            logging.error(f"Failed to initialize chatbot: {e}")
            raise

    def get_response(self, UserRequest):
        try:
            response = self.chatbot_pipeline.invoke({'UserRequest': UserRequest})
            return response
        except Exception as e:
            logging.error(f"Failed to get response: {e}")
            raise
    

def main():
    try:
        ai_service = AIService()
        
        # Sample input
        user_request = "I want upbeat pop songs with high danceability and energy."
        
        response = ai_service.get_response(user_request)
        
        print("Response:", response)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
