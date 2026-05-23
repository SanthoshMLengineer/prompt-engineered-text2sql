
from src.llm_model import LLMModel

def test_generate_sql(natural_language_query):
    llm = LLMModel(model_name="llama-3.1-8b-instant", temperature=0.7)
    sql_query = llm.generate_sql(natural_language_query)
    print("Generated SQL Query:")
    print(sql_query.content)

natural_language_query = "What are the names of all employees in the 'Sales' department?"   
test_generate_sql(natural_language_query)
    
    
