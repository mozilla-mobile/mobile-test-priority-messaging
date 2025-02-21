import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.authorization import AuthorizeResult
from dotenv import load_dotenv

load_dotenv(".env")


# Use installation_store or authorize to handle multi-workspace installations
def authorize(enterprise_id, team_id, user_id):
    # This function should retrieve the correct token from your database or storage
    # For now, let's assume you store the token in .env for testing
    token = os.getenv('SLACK_BOLT_TOKEN')

    # Return the correct token in an AuthorizeResult object
    return AuthorizeResult(
        enterprise_id=enterprise_id,
        team_id=team_id,
        bot_token=token,  # Use the bot token for this workspace
    )


# Initialize the Slack app using the authorize function
app = App(
    authorize=authorize  # This is used instead of token for multi-workspace handling
)


# @app.message()
# def handle_message_events(message, say):
#     slack_message = message.get("text")
#     slack_user = message.get("user")
#     slack_channel = message.get("channel")

#     # Log the message for debugging purposes
#     print(
#         f"Received message: {slack_message} from user {slack_user} in channel {slack_channel}"
#     )

#     if "important" in slack_message.lower():
#         print(f"Important message detected: {slack_message}")


@app.message()
def handle_message_events(message, say):
    slack_message = message.get("text")
    slack_user = message.get("user")
    slack_channel = message.get("channel")  # Get the channel the message came from

    # Log the received message
    print(f"Received message: {slack_message} from user {slack_user}")

    # Respond or send a message to the same channel
    say(f"Hey <@{slack_user}>, I received your message: {slack_message}")

    # Send a new message to the same channel
    app.client.chat_postMessage(
        channel=slack_channel, text="This is a message from the bot!"
    )


@app.event("reaction_added")
def handle_reaction_added_events(body, logger):
    logger.info(body)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_LEVEL_TOKEN"))
    handler.start()
