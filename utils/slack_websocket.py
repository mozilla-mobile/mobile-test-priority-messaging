import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv(".env")

# Initializes your app with a bot token and app-level token
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

OLLAMA_API_URL = (
    "http://localhost:8000/ollama"  # Replace with your actual Ollama endpoint
)


# Handle new messages
@app.message()
def handle_message_events(message, say):
    user = message.get("user")
    text = message.get("text")
    channel = message.get("channel")

    print(f"Message from {user} in channel {channel}: {text}")

    # Forward the message to the locally running Ollama LLM
    response = forward_to_ollama(text)

    # Optionally, you can send the response from Ollama back to the Slack channel
    if response:
        say(f"Ollama's response: {response}")
    else:
        say("Sorry, something went wrong with Ollama.")


# Function to forward text to the Ollama LLM
def forward_to_ollama(user_text):
    try:
        # Assuming Ollama takes input via POST request
        data = {"prompt": user_text}  # Adjust this based on your API format

        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract and return the response from Ollama
        ollama_response = response.json().get("response", "No response from Ollama")
        return ollama_response

    except requests.exceptions.RequestException as e:
        print(f"Error forwarding message to Ollama: {e}")
        return None


# Initialize SocketModeHandler with the app-level token
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_LEVEL_TOKEN"))
    handler.start()
