#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import os

base_template = "base.json"


def load_template(template_name) -> str:
    """
    Load a template file and return its content as a JSON string.

    Parameters:
        template_name (str): The name of the template file to load.

    Returns:
        str: A JSON string containing the contents of the template file, or None if an error occurs.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    template_path = os.path.join(parent_dir, "templates", template_name)

    try:
        with open(template_path, "r") as file:
            template_data = json.load(file)
        return json.dumps(template_data)
    except FileNotFoundError:
        print(f"Template file {template_name} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the template file {template_name}.")
        return None
    except Exception as e:
        print(f"An error occurred while loading template {template_name}: {e}")
        return None


def load_base_template() -> str:
    """
    Load the base template file and return its content as a JSON string.
    Uses caching to avoid reloading the template from the file multiple times.

    Returns:
        str: A JSON string containing the contents of the base template file, or None if an error occurs.
    """
    if not hasattr(load_base_template, "cache"):
        load_base_template.cache = load_template(base_template)
    return load_base_template.cache


def build_template(template_name) -> str:
    """
    Build a template by combining the base template with the specified template.

    Parameters:
        template_name (str): The name of the template file to build.

    Returns:
        str: A JSON string containing the combined template, or None if an error occurs.
    """
    base_template_data = load_base_template()
    if base_template_data is None:
        return None

    template_data = load_template(template_name)
    if template_data is None:
        return None

    try:
        base_template_dict = json.loads(base_template_data)
        template_dict = json.loads(template_data)
        base_template_dict["blocks"].extend(template_dict["blocks"])
        return json.dumps(base_template_dict)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the template file {template_name}.")
        return None
    except Exception as e:
        print(f"An error occurred while building template {template_name}: {e}")
        return None
