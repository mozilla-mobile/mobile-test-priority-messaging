#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
from enum import Enum

import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel


class VertexAIConfig(Enum):
    PROJECT = "moz-mobile-tools"
    LOCATION = "us-central1"
    MODEL = "gemini-1.5-flash-preview-0514"
    GENERATION_CONFIG = {"max_output_tokens": 8192, "temperature": 1, "top_p": 0.95}
    SAFETY_SETTINGS = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }


def get_system_instructions_by_name(name):
    script_dir = os.path.dirname(os.path.realpath(__file__))

    file_mapping = {
        "SRE Style Templating (Single Shot POC)": os.path.join(
            script_dir, "instructions", "system_instructions_sre.txt"
        ),
    }

    file_name = file_mapping.get(name, "")

    if not file_name:
        logging.error(f"File not found for system instruction: {name}")
        return ""

    file_path = os.path.join(script_dir, file_name)

    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"File not found for system instruction: {name}")
        return ""


def generate_content(text):
    vertexai.init(
        project=VertexAIConfig.PROJECT.value, location=VertexAIConfig.LOCATION.value
    )

    system_instruction_name = "SRE Style Templating (Single Shot POC)"
    system_instruction_text = get_system_instructions_by_name(system_instruction_name)

    model = GenerativeModel(
        VertexAIConfig.MODEL.value, system_instruction=[system_instruction_text]
    )
    responses = model.generate_content(
        [text],
        generation_config=VertexAIConfig.GENERATION_CONFIG.value,
        safety_settings=VertexAIConfig.SAFETY_SETTINGS.value,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")


def demo_text():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    demo_file_path = os.path.join(script_dir, "demo", "demo.txt")

    try:
        with open(demo_file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"Demo file not found: {demo_file_path}")
        return ""


generate_content(text=demo_text())
