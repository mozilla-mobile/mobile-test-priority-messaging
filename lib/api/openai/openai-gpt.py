#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""OpenAI API module"""

import sys
from pathlib import Path

# Append the project root to the system path for importing modules
current_script_dir = Path(__file__).resolve().parent
project_root = current_script_dir.parent.parent.parent
sys.path.append(str(project_root))


def initialize_openai_client():
    from openai import OpenAI

    from utils import get_openai_project_id, get_openai_project_service_account

    client = OpenAI()
    client.api_key = get_openai_project_service_account()
    client.project_id = get_openai_project_id()

    return client


# def send_request(prompt):
#     client = initialize_openai_client()

#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": prompt},
#         ],
#     )
#     return completion