#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this


from lib.api.google.language import analyze_entities, analyze_sentiment


def process_message(message) -> dict:
    """
    Process a message by analyzing its sentiment and entities.

    Parameters:
        message (dict): The message to process.

    Returns:
        dict: A dictionary containing the sentiment score, magnitude, and entities.
    """
    score, magnitude = analyze_sentiment(message['text'])
    entities = analyze_entities(message['text'])
    return {'score': score, 'magnitude': magnitude, 'entities': entities}


def process_score(score) -> str:
    """
    Process a sentiment score and return a corresponding sentiment label.

    Parameters:
        score (float): The sentiment score to process.

    Returns:
        str: A string representing the sentiment label.
    """
    if score > 0.25:
        return ':joy:'
    elif score < -0.25:
        return ':cry:'
    else:
        return ':thumbsup:'


def contains_keywords(text, keywords) -> bool:
    """
    Check if a text contains any of the specified keywords.

    Parameters:
        text (str): The text to check.
        keywords (list): A list of keywords to search for.

    Returns:
        bool: True if the text contains any of the keywords, False otherwise.
    """
    return any(keyword.lower() in text.lower() for keyword in keywords)


def filter_message_by_keyword(message, keywords) -> dict:
    """
    Filter a single message by a list of keywords.

    Parameters:
        message (dict): The message to filter.
        keywords (list): A list of keywords to filter by.

    Returns:
        dict: The message if it contains any of the keywords.
        None: If the message does not contain any of the keywords.
    """
    return message if contains_keywords(message['text'], keywords) else None


def process_and_filter_message(message, keywords):
    """
    Process a single message based on keywords, then analyze its sentiment and entities.

    Parameters:
        message (dict): The message to process.
        keywords (list): A list of keywords to look for.

    Returns:
        dict: A dictionary containing the sentiment score, magnitude, and entities for the message.
        None: If the message does not contain any of the specified keywords.
    """
    if contains_keywords(message['text'], keywords):
        score, magnitude = analyze_sentiment(message['text'])
        entities = analyze_entities(message['text'])
        return {'score': score, 'magnitude': magnitude, 'entities': entities}
    else:
        return None


def contains_username(message, allowed_usernames) -> bool:
    """
    Check if a message is from an allowed username.

    Parameters:
        message (dict): The message to check.
        allowed_usernames (list): A list of allowed usernames.

    Returns:
        bool: True if the message is from an allowed username, False otherwise.
    """
    return message['user'] in allowed_usernames