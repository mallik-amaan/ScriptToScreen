from src.sheet_reader import read_sheet
from src.script_generator import generate_script,setup_genai  
from dotenv import load_dotenv
import os
load_dotenv()

def main():
    SHEET_ID = os.getenv("SHEET_ID")
    SHEET_NAME = "Sheet1"

    df, records = read_sheet(
        sheet_id=SHEET_ID,
        sheet_name=SHEET_NAME,
        data_range="A1:B11"
    )

    print(df.head())       # Quick check
    print(records[:2])     # List of dicts format

    # Example: iterate through rows
    for entry in records:
        print("Title:", entry["Title"])
        print("Description:", entry["Description"])
        print("--------")
    setup_genai()
    scripts = []
    for entry in records:
        script = generate_script(entry["Title"], entry["Description"])
        scripts.append(script)
        print("Generated script:", script)
if __name__ == "__main__":
    main()
