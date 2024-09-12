from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyD9ZNTHgBhsfHOZTyhCozrJjolqaPrEMk4")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    
    try:
        # Request Markdown format in the prompt
        markdown_prompt = f"{user_message}\n\nPlease format your response in Markdown."
        response = model.generate_content(markdown_prompt)
        
        if response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"error": "No response generated"}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)