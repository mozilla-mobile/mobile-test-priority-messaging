import os
import requests
import schedule
import time
from dotenv import load_dotenv, set_key

load_dotenv()


def update_env_var(key, value, env_file=".env"):
    set_key(env_file, key, value)


# Function to refresh tokens and update .env
def refresh_access_token():
    url = "https://slack.com/api/oauth.v2.access"
    data = {
        "client_id": os.getenv("SLACK_CLIENT_ID"),
        "client_secret": os.getenv("SLACK_CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("SLACK_REFRESH_TOKEN"),
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        if token_data.get("ok"):
            access_token = token_data["access_token"]
            new_refresh_token = token_data["refresh_token"]
            expires_in = token_data["expires_in"]

            print(f"Access token refreshed. New token expires in {expires_in} seconds.")

            # Update .env with the new tokens
            update_env_var("SLACK_BOT_TOKEN", access_token)
            update_env_var("SLACK_REFRESH_TOKEN", new_refresh_token)
            return access_token, new_refresh_token
    return None, None


def schedule_token_refresh():
    schedule.every(11).hours.do(refresh_access_token)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    refresh_access_token()  # Refresh token on app startup
    schedule_token_refresh()  # Automatically refresh token every 11 hours
