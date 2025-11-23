import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

def get_google_sheet_client():
    """
    Returns an authenticated gspread client using service account credentials.
    """
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    cred_path = Path("credentials/service_account.json")

    if not cred_path.exists():
        raise FileNotFoundError("❌ Missing credentials/service_account.json file")

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        cred_path, scopes
    )

    client = gspread.authorize(creds)
    return client
