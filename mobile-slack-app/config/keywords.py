#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import os


def load_keywords():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keywords_file = os.path.join(script_dir, "keywords.json")

    """Load the allowed members from the JSON file."""
    try:
        with open(keywords_file, "r") as file:
            config = json.load(file)
        return set(config["keywords"])
    except FileNotFoundError:
        return set()
    except json.JSONDecodeError:
        return set()
    except KeyError:
        return set()
    except Exception:
        return set()
