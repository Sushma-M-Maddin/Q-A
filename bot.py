import openai
import json
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for cross-origin requests


openai.api_key = "YOUR_OPENAI_SECRET_KEY"  

# Function to load knowledge base
def load_knowledge_base():
    with open('tech_data.json', 'r') as file:
        knowledge_base = json.load(file)
    return knowledge_base

# Function to get the answer from the knowledge base
def get_answer_from_knowledge_base(query, knowledge_base):
    for entry in knowledge_base:
        if query.lower() in entry['question'].lower():
            return entry['answer']
    return None

# Function to get the answer from OpenAI
def get_answer_from_openai(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
            messages=[{"role": "user", "content": query}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I couldn't get an answer at the moment."

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests

# Route to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')  # Extract query from the incoming JSON request

    # Load the knowledge base
    knowledge_base = load_knowledge_base()

    # Check the knowledge base for an answer
    answer = get_answer_from_knowledge_base(query, knowledge_base)
    if not answer:
        # If no match is found in the knowledge base, use OpenAI
        answer = get_answer_from_openai(query)

    # Return the answer as a JSON response
    return jsonify({"answer": answer})

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
