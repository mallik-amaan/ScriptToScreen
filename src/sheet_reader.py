import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import json


def _get_credentials():
    creds_json = os.getenv("JSON")
    if not creds_json:
        raise ValueError("No JSON credentials found in environment variable 'JSON'")

    credentials_dict = json.loads(creds_json)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    return credentials


def _get_worksheet(sheet_id: str, sheet_name: str):
    """Authorize client and return worksheet object."""
    creds = _get_credentials()
    client = gspread.authorize(creds)

    try:
        sheet = client.open_by_key(sheet_id)
    except Exception as e:
        raise RuntimeError(f"Could not open sheet with ID {sheet_id}: {e}")

    try:
        worksheet = sheet.worksheet(sheet_name)
    except Exception as e:
        raise RuntimeError(f"Sheet name '{sheet_name}' not found: {e}")

    return worksheet


def read_sheet(sheet_id: str, sheet_name: str, data_range: str = "A1:B50"):
    """
    Read data from Google Sheets and return:
      - DataFrame
      - List of dicts (records)
    """

    print("Fetching sheet data...")

    worksheet = _get_worksheet(sheet_id, sheet_name)

    try:
        raw_data = worksheet.get(data_range)
    except Exception as e:
        raise RuntimeError(f"Error reading range {data_range}: {e}")

    if not raw_data or len(raw_data) < 2:
        raise ValueError("Sheet contains no usable data.")

    headers = raw_data[0]
    rows = raw_data[1:]

    df = pd.DataFrame(rows, columns=headers)
    records = df.to_dict(orient="records")

    return df, records
