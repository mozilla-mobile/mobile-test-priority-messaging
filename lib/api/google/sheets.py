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


def create_sheets_service():
    from utils import get_google_cloud_service_account

    """
    Creates a Google Sheets service object using the service account credentials.

    Returns:
        Resource: A Google Sheets service object.
    """
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    credentials = service_account.Credentials.from_service_account_file(
        get_google_cloud_service_account(), scopes=SCOPES
    )

    return build("sheets", "v4", credentials=credentials)


def update_sheet(service, spreadsheet_id, range_name, values):
    """
    Writes values to a Google Spreadsheet using the Sheets API.

    Parameters:
        service: The Google Sheets API service object.
        spreadsheet_id (str): The ID of the Google Spreadsheet.
        range_name (str): The range of cells to write to (e.g. 'Sheet1!A1').
        values (list): A list of lists containing the values to write.

    Returns:
        dict: The response from the API after writing the values.
    """
    body = {"values": values}

    return (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )


def check_spreadsheet_existence(service, spreadsheet_id):
    """
    Checks if a Google Spreadsheet with the given ID exists and is accessible by the service account.

    Parameters:
        service: The Google Sheets API service object.
        spreadsheet_id (str): The Google Spreadsheet ID to check.

    Returns:
        bool: True if the spreadsheet exists and is accessible, False otherwise.
    """
    try:
        # Attempt to get the spreadsheet, which verifies its existence and accessibility
        service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        return True
    except HttpError as error:
        if error.resp.status in [404, 403]:
            print(
                f"Spreadsheet with ID '{spreadsheet_id}' not found or access denied. HTTP error code: {error.resp.status}"
            )
        else:
            print(f"An HTTP error occurred: {error}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
