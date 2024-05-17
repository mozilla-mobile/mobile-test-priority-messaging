#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
from enum import Enum

from dotenv import find_dotenv, load_dotenv

from lib.api.google.config import get_google_cloud_credentials

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    logging.debug("No .env file found.")


class Tokens(Enum):
    SLACK_BOT_TOKEN = "SLACK_BOT_TOKEN"
    SLACK_APP_TOKEN = "SLACK_APP_TOKEN"


def get_slack_bot_token():
    """Retrieve the Slack bot token from environment variables."""
    return os.environ.get(Tokens.SLACK_BOT_TOKEN.value)


def get_slack_app_token():
    """Retrieve the Slack app token from environment variables."""
    return os.environ.get(Tokens.SLACK_APP_TOKEN.value)


def get_google_cloud_service_account():
    """Retrieve the Google Cloud application credentials from environment variables."""
    return get_google_cloud_credentials()


def get_google_sheet_id():
    """Retrieve the Google Sheet ID from environment variables."""
    return os.environ.get("GOOGLE_SHEET_ID")


def get_openai_project_service_account():
    """Retrieve the OpenAI API key from environment variables."""
    return os.environ.get("OPENAI_API_KEY")


def get_openai_project_id():
    """Retrieve the OpenAI project ID from environment variables."""
    return os.environ.get("OPENAI_PROJECT_ID")
