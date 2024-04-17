#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.middleware import IgnoringSelfEvents

from lib.api.google.language import analyze_entities, analyze_sentiment
from message import process_message, process_score
from utils import get_slack_app_token, get_slack_bot_token


def setup_logging():
    """Setup logging configuration."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)


def setup_app() -> App:
    try:
        app = App(token=get_slack_bot_token())
        app.middleware(IgnoringSelfEvents())
        return app
    except Exception as e:
        logging.error(f"Failed to setup the app: {e}")


def setup_message_listeners(app):
    @app.message()
    def message(message, say):

        processed_message = process_message(message)
        logging.debug(f"Sentinment Score: {processed_message['score']}")
        logging.debug(f"Entities: {processed_message['entities']}")

        say(f"{process_score(processed_message['score'])}")

        score, magnitude = analyze_sentiment(message["text"])
        entities = analyze_entities(message["text"])

        logging.debug(f"Sentiment Score: {score}, Magnitude: {magnitude}")
        logging.debug(f"Entities: {entities}")

    @app.message(re.compile("Help", re.IGNORECASE))
    def message_help(message, say):
        pass


def setup_slash_command_listeners(app):
    @app.command("/help")
    def command_echo(ack, say, command):
        ack()
        say(f"You used the command: {command['command']} with text: {command['text']}")


def main():
    setup_logging()
    app = setup_app()
    if app is not None:
        setup_message_listeners(app)
        setup_slash_command_listeners(app)
        SocketModeHandler(app, get_slack_app_token()).start()
    else:
        logging.error("Failed to setup the app.")


if __name__ == "__main__":
    main()
