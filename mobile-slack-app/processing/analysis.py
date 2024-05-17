#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


"""This module contains functions for assessing the relevancy of messages.
   The relevancy of a message is determined by the presence of keywords in the message text.
   As well determined by the classification of the message passed through machine-learning to determine
   the relevancy of the message: nature of the event, the urgency of the event, target audience, and the
   action to be taken.
"""

def process_relevancy()