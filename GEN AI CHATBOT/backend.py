from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS  # Allow frontend to communicate with backend

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure API key securely (Replace with your actual API key)
genai.configure(api_key="AIzaSyAAzXyXt_mPPgY_JPnTmDM0qFZu764-_IQ")  

# Define the chatbot model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def generateResponse(input_text):
    response = model.generate_content([
        "you are a gameplan chatbot, so reply accordingly",
        "input: who are you",
        "output: I'm a gameplan chatbot",
        f"input: {input_text}",
        "output: "
    ])
    return response.text  # Extract text from the response

# Flask API Route to Handle Chat Requests
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"response": "Please provide a message!"})
    
    bot_reply = generateResponse(user_message)
    
    return jsonify({"response": bot_reply})

# Run the API Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
