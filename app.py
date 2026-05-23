from flask import Flask, request, session, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

from src.llm_model import LLMModel

# Initialize the LLM model
llm = LLMModel(model_name="llama-3.1-8b-instant", temperature=0.7)

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
            max-width: 600px;
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
            padding: 10px;
            border-radius: 10px;
            max-width: 70%;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }
        .bot-message {
            background-color: #e9ecef;
            color: black;
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
        }
        .chat-input button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .chat-input button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-messages">
            {% for msg in messages %}
            <div class="message {{ 'user-message' if msg.type == 'user' else 'bot-message' }}">{{ msg.text }}</div>
            {% endfor %}
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
    messages = session.get('messages', [{'type': 'bot', 'text': "Hello! I'm here to help you convert natural language queries to SQL. Ask me anything!"}])
    return render_template_string(HTML_TEMPLATE, messages=messages)

@app.route('/chat', methods=['POST'])
def chat():
    query = request.form.get('query', '').strip()
    if not query:
        messages = session.get('messages', [])
        return render_template_string(HTML_TEMPLATE, messages=messages)
    
    # Get current messages
    messages = session.get('messages', [{'type': 'bot', 'text': "Hello! I'm here to help you convert natural language queries to SQL. Ask me anything!"}])
    
    # Add user message
    messages.append({'type': 'user', 'text': query})
    
    try:
        print(f"Received query: {query}")
        response = llm.generate_sql(query)
        sql = response.content
        messages.append({'type': 'bot', 'text': sql})
    except Exception as e:
        messages.append({'type': 'bot', 'text': f'Sorry, there was an error: {str(e)}'})
    
    # Save to session
    session['messages'] = messages
    
    return render_template_string(HTML_TEMPLATE, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)