import openai
from flask import Flask, request, jsonify, render_template

# Set the API base URL and your API key
openai.api_base = "https://api.groq.com/openai/v1"  # Replace with your actual API URL if necessary
openai.api_key = "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"  # Replace with your actual API key

# Initialize the conversation history
conversation_history = [
    {"role": "system", "content": "You are an expert on Composite Labs and Monad. Focus only on those topics."}
]

# Create the Flask app
app = Flask(__name__)

# Route for the welcome message and main page with user input form
@app.route("/")
def welcome():
    return render_template("index.html")

# Route to handle chat interactions
@app.route("/chat", methods=["POST"])
def chatbot():
    user_input = request.form.get("message")  # Get the message from the form
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Add the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Call the OpenAI API for chat completion
        response = openai.ChatCompletion.create(
            model="llama-3.3-70b-versatile",  # Use a Llama model, replace if necessary
            messages=conversation_history,
            temperature=0.5,
            max_tokens=256,
            top_p=1.0
        )

        # Extract and send the assistant's response
        assistant_message = response["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": assistant_message})

        return render_template("index.html", user_input=user_input, assistant_response=assistant_message)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main entry point for the app
if __name__ == "__main__":
    # Run the app on all IPs (0.0.0.0) and port 5000
    app.run(host="0.0.0.0", port=5000)
