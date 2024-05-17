import os
import threading
import time
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Google API Key from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure GenAI with the Google API Key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-pro')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json  # Extract JSON data sent from frontend
    user_question = data.get('question')  # Extract question from JSON data
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    # Generate response using the generative model
    response = model.generate_content(user_question)

    # Convert the response to a serializable format
    response_text = response.text

    # Return the response to the frontend
    return jsonify({"answer": response_text}), 200

def keep_alive():
    while True:
        try:
            # Send a request to your Flask application's URL to keep it alive
            requests.get('https://your-app-url.onrender.com')
        except Exception as e:
            print(f"Keep-alive request failed: {e}")
        # Wait for 1 minute
        time.sleep(60)

if __name__ == "__main__":
    app.run(debug=True)
