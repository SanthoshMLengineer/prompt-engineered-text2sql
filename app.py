from flask import Flask, request, session, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

from src.llm_model import LLMModel

# Initialize the LLM model
llm = LLMModel(model_name="llama-3.1-8b-instant", temperature=0)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NLP to SQL Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .chat-container {
            width: 100%;
            max-width: 800px;
            height: 80vh;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            border-bottom: 1px solid #eee;
        }
        .message {
            margin-bottom: 15px;
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
        }
        .query-section {
            margin-bottom: 15px;
            color: #0056b3;
            font-weight: bold;
            font-size: 1.1em;
        }
        .query-text {
            color: #333;
            font-weight: normal;
        }
        .explanation-section {
            color: #28a745;
            font-weight: bold;
            font-size: 1.1em;
        }
        .explanation-text {
            color: #333;
            font-weight: normal;
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            white-space: pre-wrap;
            font-family: monospace;
            margin-top: 10px;
            border-left: 4px solid #28a745;
        }
        .error-text {
            color: #dc3545;
            font-weight: bold;
        }
        .chat-input {
            padding: 20px;
        }
        .chat-input form {
            display: flex;
        }
        .chat-input input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-right: 10px;
            font-size: 1em;
        }
        .chat-input button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
        }
        .chat-input button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-messages">
            {% if error %}
            <div class="message">
                <div class="error-text">Error: {{ error }}</div>
            </div>
            {% elif query %}
            <div class="message">
                <div class="query-section">Query: <span class="query-text">{{ query }}</span></div>
                <div class="explanation-section">Explanation:
                    <div class="explanation-text">{{ sql }}</div>
                </div>
            </div>
            {% else %}
            <div class="message">
                <div class="explanation-section">Hello! I'm here to help you convert natural language queries to SQL. Please feel free to ask me anything!<br><br><span style="font-weight: normal; font-size: 0.9em; color: #555;"><i>Please note: As I am currently running on a free-tier API, I can kindly accommodate up to 2 queries per session. Thank you for your understanding!</i></span></div>
            </div>
            {% endif %}
        </div>
        <div class="chat-input">
            <form method="post" action="/chat">
                <input type="text" name="query" placeholder="Enter your natural language query..." required>
                <button type="submit">Send</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, query=None, sql=None, error=None)

@app.route('/chat', methods=['POST'])
def chat():
    query = request.form.get('query', '').strip()

    if not query:
        return render_template_string(HTML_TEMPLATE, query=None, sql=None, error=None)
    
    counter = session.get('counter', 0) + 1
    session['counter'] = counter
    if counter > 2:
        error_msg = "Thank you so much for using this service! To ensure fair usage on our free tier, I can currently only process up to 2 queries per session. I would be delighted to assist you further if you try again a little later. Have a wonderful day!"
        return render_template_string(HTML_TEMPLATE, query=query, sql=None, error=error_msg)
    
    try:
        print(f"Received query: {query}")
        response = llm.generate_sql(query)
        sql = response.content
        return render_template_string(HTML_TEMPLATE, query=query, sql=sql, error=None)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, query=query, sql=None, error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)