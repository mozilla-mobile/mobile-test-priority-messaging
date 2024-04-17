#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os


def get_google_cloud_credentials():
    """
    Checks if the GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    If set, returns the path to the service account key file.
    Raises an error if the environment variable is not set, indicating
    that the application is not properly configured for authentication.
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credentials_path:
        raise EnvironmentError(
            "The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set. "
            "Please set it to the path of your service account key JSON file before running the application."
        )

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            "The service account key file specified in GOOGLE_APPLICATION_CREDENTIALS does not exist. "
            "Please check the path and try again."
        )

    return credentials_path
