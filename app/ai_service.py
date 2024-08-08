from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

class AIService:
    def __init__(self):
        self.chatbot_pipeline = self.initialise_llama3()

    def initialise_llama3(self):
        try:
            create_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are my personal assistant"),
                    ("user", "Question: {question}")
                ]
            )

            lamma_model = Ollama(model="llama3.1")
            format_output = StrOutputParser()

            chatbot_pipeline = create_prompt | lamma_model | format_output
            return chatbot_pipeline
        except Exception as e:
            logging.error(f"Failed to initialize chatbot: {e}")
            raise

    def get_response(self, question):
        try:
            response = self.chatbot_pipeline.invoke({'question': question})
            return response
        except Exception as e:
            logging.error(f"Failed to get response: {e}")
            raise
