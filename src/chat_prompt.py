from langchain_core.prompts import ChatPromptTemplate

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
    