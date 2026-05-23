from os import getenv

from langchain_groq import ChatGroq
from src.chat_prompt import Chatprompt

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
GROQ_API_KEY = getenv("GROQ_API_KEY")  # Get the API key from environment variables

class LLMModel:
    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.model = ChatGroq(model=self.model_name,
                              groq_api_key=GROQ_API_KEY,
                              temperature=self.temperature)
    
    def generate_sql(self, natural_language_query: str):
        self.chat_prompt = Chatprompt()
        prompt = self.chat_prompt.format_prompt(
            natural_language_query=natural_language_query
            )
        response = self.model.invoke(prompt)
        return response

"""
llm = LLMModel(model_name="llama-3.1-8b-instant", temperature=0.7)
natural_language_query = "What are the names of all employees in the 'Sales' department?"   
sql_query = llm.generate_sql(natural_language_query)
print("Generated SQL Query:")
print(sql_query.content)
"""
