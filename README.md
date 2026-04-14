# Script2Screen

## Overview
Script2Screen is a Python-based pipeline that turns topic inputs from Google Sheets into narrated explainer videos. It combines LLM-powered script generation, text-to-speech narration, and automated video assembly into a single Streamlit workflow. The main purpose is to speed up short-form educational or product-content production with minimal manual editing.

## Features
- Reads structured content from a Google Sheet (`Title`, `Description`) using the Google Sheets API.
- Generates narration-ready scripts with Google Gemini.
- Produces English voice narration using gTTS.
- Assembles MP4 videos with text-based scenes and synced audio using MoviePy + Pillow.
- Provides an interactive Streamlit UI for end-to-end execution and preview.
- Exports generated artifacts into organized output folders (`narration/`, `output/`).

## Tech Stack
- Language: Python 3.10+
- Key Dependencies:
	- `streamlit` (UI)
	- `google-generativeai` (Gemini integration)
	- `gspread`, `oauth2client` (Google Sheets access)
	- `gTTS` (text-to-speech)
	- `moviepy`, `numpy`, `pillow`, `imageio-ffmpeg` (video/audio processing)
	- `pandas` (data handling)
- Tools:
	- `pip` + `requirements.txt` for dependency management
	- Google Cloud service account credentials for Sheets authentication

## Installation

### Prerequisites
- Python 3.10 or newer
- `ffmpeg` installed and available in PATH (required by MoviePy)
- A Google Cloud service account with access to the target Google Sheet
- Gemini API key (Google AI Studio / Google Cloud)

### Setup Steps
```bash
# Clone the repository
git clone [repo-url]

# Navigate to directory
cd Script2Screen

# (Optional) Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the project
streamlit run main.py
```

## Project Structure
- `main.py`: Streamlit entrypoint and end-to-end workflow orchestration.
- `src/sheet_reader.py`: Reads and validates Google Sheet content.
- `src/script_generator.py`: Gemini setup, prompting, and script generation.
- `src/tts_generator.py`: Narration generation via gTTS.
- `src/video_assembler.py`: Scene rendering and final MP4 creation.
- `src/google_client.py`: Alternate helper for service-account-based Google auth.
- `credentials/`: Local credential files (should be excluded from public repos).
- `data/`: Working data directories (`audios/`, `sheets/`, `slides/`, `videos/`).
- `narration/`: Generated narration audio files.
- `output/`: Final rendered videos.
- `notebooks/`, `Script2Screen.ipynb`: Notebook-based experimentation.

## Usage
1. Start the app:
	 ```bash
	 streamlit run main.py
	 ```
2. Open the Streamlit URL shown in terminal.
3. Paste a Google Sheet URL containing columns like `Title` and `Description`.
4. Share the sheet with your service account email (`SERVICE_EMAIL`) with edit/view access as needed.
5. Click **Generate Videos** to run the pipeline for each row.

Expected outputs:
- Narration audio files in `narration/`.
- Rendered videos in `output/` (for example, `output/video_0.mp4`).

## Configuration
Set these environment variables before running:

- `GEMINI_API_KEY`: API key used by `src/script_generator.py`.
- `JSON`: Full JSON string of Google service account credentials (used by `src/sheet_reader.py`).
- `SERVICE_EMAIL`: Service account email shown in UI for sheet-sharing guidance.

Example:
```bash
export GEMINI_API_KEY="your_gemini_api_key"
export SERVICE_EMAIL="service-account@project.iam.gserviceaccount.com"
export JSON='{"type":"service_account", ... }'
```

Notes:
- `src/google_client.py` expects `credentials/service_account.json`, while the active app flow uses the `JSON` environment variable. Keep your auth strategy consistent.
- Never commit real credentials to source control.

## Development
- Development setup:
	- Use a virtual environment (`.venv`) and install from `requirements.txt`.
	- Run locally with `streamlit run main.py`.
- Testing:
	- No automated test suite is currently included in the repository.
	- Recommended: add `pytest` tests for `src/script_generator.py`, `src/sheet_reader.py`, and `src/video_assembler.py`.
- Code style guidelines:
	- Follow PEP 8 for Python formatting and naming.
	- Keep modules single-purpose and side-effect aware.
	- External API/credential access should remain environment-driven.

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Make focused, well-documented changes.
4. Validate locally (`streamlit run main.py`) and include reproducible steps in your PR.
5. Open a pull request with a clear summary of changes and rationale.

## License
No license file is currently present. Add a `LICENSE` file (for example, MIT, Apache-2.0, or GPL-3.0) and update this section accordingly.

## Contact
- Maintainer: [Your Name]
- LinkedIn: [Your LinkedIn URL]
- Portfolio: [Your Portfolio URL]

---

If you plan to publish this project, replace placeholder values (`[repo-url]`, contact details, and final license) before release.
