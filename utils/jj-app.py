import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.middleware import IgnoringSelfEvents

from dotenv import load_dotenv

load_dotenv(".env")

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("REDDIT_POST")
def message_hello(message, say):
    def is_bug_post(
        post_text,
        keywords=["does not work", "bug", "issue", "problem", "error", "crash"],
    ):
        """
        Determine if a post is about a bug or defect based on specific keywords.

        Args:
        - post_text (str): The text of the Reddit post.
        - keywords (list): A list of keywords or phrases indicative of a bug report.

        Returns:
        - bool: True if the post is likely about a bug, False otherwise.
        """
        post_text_lower = post_text.lower()
        print(message)
        return any(keyword in post_text_lower for keyword in keywords)

    bug_notification_message = (
        f"🐞 *New Bug Report Detected*\n*Title:* {message['text']}...\n"
    )
    if is_bug_post(message["text"]):
        say("This post appears to be about a bug. I'll notify the team.")
        # dm user
        response = app.client.chat_postMessage(
            channel=f'@{user['something']}, text=bug_notification_message'
        )


@app.view("dashboard_preview")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
