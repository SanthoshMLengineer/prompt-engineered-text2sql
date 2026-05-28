from langchain_core.prompts import ChatPromptTemplate

from langchain_groq import ChatGroq 
from dotenv import load_dotenv

#from .logging_utils import logger

load_dotenv()   

def generate_sql(user_input):   
    try:
        # Initialize Groq LLM
        sql_llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.0
        )

        examples = [
             ('system', 
             "You are an AI assistant that mainly writes sql queries from the text input\n"
             "Rules:\n"
             "1. If user greets you (like 'hi', 'hello', 'hey'), greet them back politely and offer SQL help.\n"
             "2. If user gives a data-related input, respond ONLY with the correct SQL query.\n"
             "3. If input is unrelated to SQL or greetings, politely say you only generate SQL queries."
             ),
             ('human', 'hi'),
             ("ai", "Hello! I am your SQL assistant. How can I help you with queries today?"),
             ('human', 'Explain Machine Learning'),
             ("ai", "I am designed only to generate SQL queries. Could you please provide a SQL-related request?"),
             ('human', 'Explain SQL'),
             ('ai', 'Ask to generate the sql query like given total no of orders'),
             ("human", "Total number of orders in orders table"),
             ("ai", "SELECT COUNT(*) AS total_orders FROM orders;"),
             ("human", "List all customers in customer table"),
             ("ai", "SELECT * FROM customer;"),
             ('human', '{input}')
        ]

        example_prompt = ChatPromptTemplate.from_messages(examples)
        formatted_prompt = example_prompt.format_messages(input=user_input)
        
        result = sql_llm.invoke(formatted_prompt)
        logger.info("SQL AI generated a query successfully.")
        return dict({"sql": result})
    except Exception as e:
        logger.error(f"Something went wrong while generating SQL: {e}", exc_info=True)
        return dict({"error": str(e)})
    
class Chatprompt:
    def __init__(self):
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "You are an assistant taht converts natural language queries into SQL queries."
                ),
                ("human", "hello world"),
                ("ai", "Hello! how can i assist you with SQL queries today?"),

                ("human", "What is data science?"),
                ("ai", "I am here to help to convert natural language queries into SQL queries. Please provide a natural language query related to SQL, and I will generate the corresponding SQL query for you."),

                ("human", "{query}")

            ]
        )
    
    def format_prompt(self, natural_language_query: str):
        return self.prompt_template.format_messages(query=natural_language_query)
    