from flask import Flask, request, jsonify
# flask is providing the web server
# request is used to get the data from the client
# jsonify is used to convert the data to JSON format and send it to the client
from flask_cors import CORS
# CORS is used to allow the client to make requests to the server 
import google.generativeai as genai
# generativeai is used to generate the response and also to configure the API key
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_AI_API_KEY")
genai.configure(api_key=api_key)
#  Configures the Google AI service with the special key.
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#  Sets up the model you want to use from Google AI.

app = Flask(__name__)
#  Creates a new web server using Flask.
CORS(app)
#Allows your server to accept requests from different sources like chat bot

@app.route('/chat', methods=['POST'])
# Defines a URL path /chat that accepts POST requests (when your  vhat bot sends a message).
def chat():
    data = request.json
    # Gets the data sent by your chat bot.
    user_message = data['message']
    #  Extracts the user’s message from the data
    
    try:
        # Request Markdown format in the prompt
        markdown_prompt = f"{user_message}\n\nPlease format your response in Markdown."
        #  Prepares the message to be sent to Google AI in Markdown format.

        response = model.generate_content(markdown_prompt)
        #  Asks Google AI to generate a response based on the message.
        
        if response.text:
        #: Checks if there is a response.
            return jsonify({"response": response.text})
        # Sends the response back to your chat bot in JSON format.
        else:
            return jsonify({"error": "No response generated"}), 500
        # If no response, sends an error message.
    except Exception as e:
    #  Catches any errors that occur
        print(f"An error occurred: {e}")
        #  Prints the error message to the console.
        return jsonify({"error": "An error occurred while processing your request"}), 500
        #  Sends an error message back to your chat bot in JSON format.

if __name__ == '__main__':
# Checks if this script is being run directly.
    app.run(debug=True, port=3009)
    #  Starts the server on port 3009 with debugging enabled.
