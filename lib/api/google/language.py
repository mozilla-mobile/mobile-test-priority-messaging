#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from google.api_core.exceptions import GoogleAPICallError, InvalidArgument
from google.cloud import language_v2

"""Google Cloud Natural Language API sentiment analysis."""


def analyze_entities(text) -> list:
    """
    Analyzes the entities in a given text using the Google Cloud Natural Language API.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list: A list of entities found in the text.
    """
    try:
        client = language_v2.LanguageServiceClient()
        document = language_v2.Document(
            content=text, type_=language_v2.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_entities(request={"document": document})
        entities = response.entities
        return entities
    except InvalidArgument as invalid_arg:
        raise invalid_arg
    except GoogleAPICallError as api_error:
        raise api_error
    except Exception as exception:
        raise exception


def analyze_sentiment(text) -> tuple:
    """
    Analyzes the sentiment of a given text using the Google Cloud Natural Language API.

    Parameters:
        text (str): The text to analyze.

    Returns:
        tuple: A tuple containing the sentiment score and magnitude.
    """
    try:
        client = language_v2.LanguageServiceClient()
        document = language_v2.Document(
            content=text, type_=language_v2.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(request={"document": document})
        sentiment = response.document_sentiment
        return sentiment.score, sentiment.magnitude
    except InvalidArgument as invalid_arg:
        raise invalid_arg
    except GoogleAPICallError as api_error:
        raise api_error
    except Exception as exception:
        raise exception
