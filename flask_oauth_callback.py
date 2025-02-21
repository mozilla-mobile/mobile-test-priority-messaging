# flask_oauth_callback.py

from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv, set_key

load_dotenv()

app = Flask(__name__)
CORS(app)


# Function to update the .env file with new tokens
def update_env_var(key, value, env_file=".env"):
    set_key(env_file, key, value)


@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    if code:
        # Exchange authorization code for access and refresh tokens
        response = requests.post(
            "https://slack.com/api/oauth.v2.access",
            data={
                "client_id": os.getenv("SLACK_CLIENT_ID"),
                "client_secret": os.getenv("SLACK_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": os.getenv("REDIRECT_URI"),
            },
        )

        if response.status_code == 200:
            token_data = response.json()
            if token_data.get("ok"):
                access_token = token_data["access_token"]
                refresh_token = token_data["refresh_token"]

                # Store the tokens securely
                update_env_var("SLACK_BOT_TOKEN", access_token)
                update_env_var("SLACK_REFRESH_TOKEN", refresh_token)

                return jsonify(
                    {"status": "success", "message": "App installed successfully!"}
                )

    return jsonify({"status": "error", "message": "App installation failed."}), 400


if __name__ == "__main__":
    app.run(port=5299)
