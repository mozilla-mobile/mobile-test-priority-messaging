#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json


class SlackMessageFormatter:
    @staticmethod
    def format_slack_message(template_data_str):
        """
        Convert a JSON string from a template into Slack block format.

        Parameters:
            template_data_str (str): JSON string containing template data.

        Returns:
            list: A list of dictionaries formatted as Slack blocks.
        """
        try:
            # Convert JSON string back to dictionary
            template_data = json.loads(template_data_str)
            # Return the blocks directly if they exist
            return template_data.get('blocks', [])
        except json.JSONDecodeError:
            print("Error decoding JSON string.")
            return []
        except Exception as e:
            print(f"An error occurred while formatting the Slack message: {e}")
            return []
