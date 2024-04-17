#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

current_script_dir = Path(__file__).resolve().parent
project_root = current_script_dir.parent.parent.parent
sys.path.append(str(project_root))


"""Google Sheets API utility functions."""


def check_spreadsheet_existence():
    from utils import get_google_cloud_service_account, get_google_sheet_id

    """
    Checks if a Google Spreadsheet with the given ID exists and is accessible by the service account.

    Parameters:
        spreadsheet_id (str): The Google Spreadsheet ID to check.

    Returns:
        bool: True if the spreadsheet exists and is accessible, False otherwise.
    """
    try:
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        credentials = service_account.Credentials.from_service_account_file(
            get_google_cloud_service_account(), scopes=SCOPES)

        service = build('sheets', 'v4', credentials=credentials)
        return service.spreadsheets().get(spreadsheetId=get_google_sheet_id()).execute()
    except HttpError as error:
        if error.resp.status in [404, 403]:
            raise Exception(f"Spreadsheet with ID '{get_google_sheet_id()}' not found or access denied.")
        else:
            print(f"An HTTP error occurred: {error}")
        return False
    except Exception as e:
        raise e("An error occurred while checking the spreadsheet existence.")
        return False


exists = check_spreadsheet_existence()
print(f"Spreadsheet exists: {exists}")
