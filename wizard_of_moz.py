# wizard_of_moz.py

import os
import time
import subprocess
import requests
import json
import hmac
import hashlib
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.authorization import AuthorizeResult
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Ollama
from dotenv import load_dotenv, set_key
from formulaic_app import get_llm_response, get_formula_metadata

load_dotenv()

wiz_moz_webhook = (os.getenv('WIZ_MOZ_WEBHOOK'))
message_broker_wh = os.getenv('SLACK_MESSAGE_BROKER_WEBHOOK')
slack_bot_token = os.getenv('SLACK_BOLT_TOKEN')
recipe_group = {
    "priority": {"recipe_id": "7e8a9c69-61ca-4a9e-8b79-49980b85db55"},
    "platform": {"recipe_id": "1234", "script_id": "5678"},
    "summarize_event": {"recipe_id": "1234", "script_id": "5678"},
}

# Load examples from examples.txt to cache them in memory
# def load_examples(file_path):
#     with open(file_path, "r") as file:
#         examples = file.read()
#     return examples


# Cached examples from the examples.txt file
# examples_cache = load_examples("./data/examples.txt")

# Define the Prompt Template, reusing the cached examples
# multi_shot_prompt = PromptTemplate(
#     input_variables=["message"],
#     template=f"""
#     You are an assistant that helps classify Slack messages based on priority. Here are some examples:

#     {examples_cache}

#     Now, classify the following message:
#     Message: {{message}}
#     Classification:
#     """,
# )

# llm = Ollama(model="llama3.1:8b-instruct-q8_0")

# Create a LangChain chain for classification
# classification_chain = LLMChain(llm=llm, prompt=multi_shot_prompt)


# Function to classify a message and return True if high priority
# def is_high_priority(message):
#     high_priority_phrases = [
#         "@Jackie",
#         "beta release tests failing",
#         "nightly release tests failing",
#         "the test you wrote is failing",
#     ]

#     for phrase in high_priority_phrases:
#         if phrase.lower() in message.lower():
#             return True

#     classification = classification_chain.run({"message": message})
#     return "High Priority" in classification


# Function to trigger the alert window using subprocess
# def trigger_alert_window(user, message, channel):
#     subprocess.Popen(
#         ["python3", "annoying_alert.py", "High Priority Alert", user, message, channel]
#     )


# Function to send data to Slack workflow webhook
# def send_to_slack_webhook(user, message, channel):
#     data = {"user": user, "message": message, "channel": channel, "priority": "High"}

#     # Send the POST request to the webhook URL
#     response = requests.post(
#         slack_workflow_webhook_url,
#         data=json.dumps(data),
#         headers={"Content-Type": "application/json"},
#     )

#     if response.status_code == 200:
#         print("Successfully sent data to the Slack webhook.")
#     else:
#         print(f"Failed to send data: {response.status_code}, {response.text}")

# @app.message()
# def handle_message_events(message, say):
#     slack_message = message.get("text")
#     slack_user = message.get("user")
#     slack_channel = message.get("channel")  # Get the channel the message came from

#     # Classify the Slack message (returns True if high priority)
#     if is_high_priority(slack_message):
#         print(f"High priority message detected: {slack_message}")

#         # Trigger the alert window
#         trigger_alert_window(slack_user, slack_message, slack_channel)

#         # Send high-priority message data to Slack workflow webhook
#         send_to_slack_webhook(slack_user, slack_message, slack_channel)
# Initialize the Slack app and refresh token before use

# load_dotenv(".env")

# OAuth token settings
# client_id = os.getenv("TEST_APP_CLIENT_ID")
# client_secret = os.getenv("SLACK_CLIENT_SECRET")
# refresh_token = os.getenv("SLACK_REFRESH_TOKEN")
# bot_token = os.getenv("SLACK_BOT_TOKEN")
# workflow_webhook_url = os.getenv("PRIORITY_ALERT_PUSH_EVENT_WORKFLOW")
# app_level_token = os.getenv("SLACK_APP_LEVEL_TOKEN")
# signing_secret = os.getenv("TEST_APP_SIGNING_SECRET")

# Initialize the Slack app using the bot token
# app = App(token=os.getenv('TEST_APP_TOKEN'))


# Verifying requests from Slack (use your signing secret)
def verify_slack_request(request, signing_secret):
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    slack_signature = request.headers.get("X-Slack-Signature")

    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False  # Prevent replay attacks

    request_body = request.get_data(as_text=True)
    sig_basestring = f"v0:{timestamp}:{request_body}"

    my_signature = (
        "v0="
        + hmac.new(
            signing_secret.encode("utf-8"),
            sig_basestring.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
    )

    return hmac.compare_digest(my_signature, slack_signature)


# @app.middleware  # Verifies each request using signing secret
# def verify_request(context, payload, next):
#     request = context["request"]

#     if not verify_slack_request(request, signing_secret):
#         print("Request verification failed.")
#         return  # Block the request if it fails verification


#     return next()
# Use installation_store or authorize to handle multi-workspace installations
async def authorize(enterprise_id, team_id):
    # This function should retrieve the correct token from your database or storage
    # For now, let's assume you store the token in .env for testing
    token = slack_bot_token

    # Return the correct token in an AuthorizeResult object
    return AuthorizeResult(
        enterprise_id=enterprise_id,
        team_id=team_id,
        bot_token=token,  # Use the bot token for this workspace
    )


# Initialize the Slack app using the authorize function
app = AsyncApp(
    authorize=authorize  # This is used instead of token for multi-workspace handling
)


@app.message()
async def handle_message_events(message, say, ack):
    slack_message = message.get("text")
    # temp message tag for testing
    if not "[TEST]" in slack_message:
        print("ignoring old message from the very long message queue...")
        return
    # Ignore self-generated messages
    if message.get("bot_id"):
        print("Ignoring message from this bot.")
        return

    # Ignore messages with the LLM marker
    if "[IGNORE-FLAG]" in slack_message:
        print("Ignoring LLM response message.")
        return

    slack_user = message.get("user")
    slack_channel = message.get("channel")  # Get the channel the message came from

    # Log the received message
    print(f"Received message: {slack_message} from user {slack_user}")
    await ack()
    # formulaic_response = await get_llm_response(slack_message)
    formula_opts = {"recipe_id": recipe_group["priority"]["recipe_id"]}
    # formula_options = await get_formula_metadata(recipe_id)
    priority = await get_llm_response(slack_message, formula_opts)
    # formulaic_response = await get_formula_metadata()
    # print(f"{formulaic_response=}")
    # slack_webhook = wiz_moz_webhook
    slack_webhook = message_broker_wh
    message_broker_wh_payload = {
        "platform": "iOS",
        "event": "Major Fire",
        "priority": "High",
        "event_ref": "pretend event",
    }
    test_message_broker_wh_payload = {
        "platform": "iOS",
        "event": "Major Fire",
        "priority": priority,
        "event_ref": "https://mozilla.slack.com/archives/C07RS0GML5N/p1731012968469689",
    }
    print(f"{test_message_broker_wh_payload=}")
    print(f"{priority=}")
    # priority = formulaic_response[0]["chat"]["messages"][3]["content"]
    # print(priority)
    # owner = formulaic_response[0]["chat"]["messages"][5]["content"]
    # print(f"{owner=}")
    # slack_wh_message = {"text": f"[PRIORITY]: {priority} \n[OWNER]: {owner}"}
    # print(f"{slack_wh_message=}")
    # response = requests.post(slack_webhook, json=slack_wh_message)
    response = requests.post(slack_webhook, json=test_message_broker_wh_payload)


# add slash command support with event listener for /subscribe events
# /subscribe corresponds to a slack canvas of the same name
# if canvas doesn't exist, create canvas
# add user_id to slack canvas
# https://tools.slack.dev/bolt-python/concepts/socket-mode
# def setup_slash_command_listeners(app):
# @app.command("/help")
# def command_echo(ack, say, command):
#     ack()
#     say(f"You used the command: {command['command']} with text: {command['text']}")

# Forward the webhook data to Slack
# test_slack_message = {"text": f"Received webhook event: {response}"}

# Send the request to Slack
# test_response = requests.post(slack_webhook_url, json=slack_wh_message)
# print(response)
# Respond or send a message to the same channel
# say(f"Hey <@{slack_user}>, I received your message: {slack_message}")

# # Send a new message to the same channel
# app.client.chat_postMessage(
#     channel=slack_channel, text="This is a message from the bot!"
# )


# @app.event("reaction_added")
# def handle_reaction_added_events(body, logger):
#     logger.info(body)


async def main():
    handler = AsyncSocketModeHandler(
        app, os.getenv('TEST_APP_TEST_TOKEN_ID')
    )
    await handler.start_async()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
