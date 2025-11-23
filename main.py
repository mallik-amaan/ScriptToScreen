# app.py
import streamlit as st
import os
from urllib.parse import urlparse, parse_qs
from src.sheet_reader import read_sheet
from src.script_generator import generate_script, setup_genai
from src.tts_generator import generate_narration
from src.video_assembler import build_video

# ===== Streamlit Page Config =====
st.set_page_config(page_title="Script2Screen", layout="wide", page_icon="🎬")

st.markdown("<h1 style='text-align: center; color: #4B0082;'>🎬 Script2Screen: Google Sheets to Video</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #4B0082;'>Enter your Google Sheet URL and generate videos step by step</h4>", unsafe_allow_html=True)
st.write("---")

# ===== Input Google Sheet URL =====
sheet_url = st.text_input(
    "Enter your Google Sheet URL:",
    "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0"
)

if sheet_url:
    # Extract Sheet ID
    try:
        parsed = urlparse(sheet_url)
        if "/d/" in parsed.path:
            sheet_id = parsed.path.split("/d/")[1].split("/")[0]
        else:
            qs = parse_qs(parsed.query)
            sheet_id = qs.get("id", [None])[0]

        if not sheet_id:
            st.error("Could not extract Sheet ID. Please check your URL.")
        else:
            st.success(f"✅ Extracted Sheet ID: {sheet_id}")

            st.info("⚠️ Please share the Google Sheet with the service email below with Edit access:")
            st.code(os.getenv("SERVICE_EMAIL"))

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("Generate Videos", use_container_width=True):
                    # Setup GenAI
                    setup_genai()

                    # Read Sheet
                    df, records = read_sheet(sheet_id=sheet_id, sheet_name="Sheet1", data_range="A1:B11")
                    st.markdown("<h4 style='text-align: center;'>Preview of your Google Sheet</h4>", unsafe_allow_html=True)
                    st.dataframe(df.head())

                    # Process each row
                    for idx, entry in enumerate(records):
                        title = entry["Title"]
                        description = entry["Description"]

                        st.markdown(f"<h3 style='text-align: center; color:#4B0082;'>Processing: {title}</h3>", unsafe_allow_html=True)

                        # ===== Script Generation =====
                        st.markdown("**Step 1: Generating Script...**")
                        script_bar = st.progress(0)
                        script = generate_script(title, description)
                        script_bar.progress(100)
                        st.success("✅ Script generated!")
                        narration_text = script["script"]

                        # ===== Audio Generation =====
                        st.markdown("**Step 2: Generating Narration Audio...**")
                        audio_bar = st.progress(0)
                        # If generate_narration supports yielding progress
                        for prog in generate_narration(narration_text, f"narration/narration_{idx}.mp3"):
                            audio_bar.progress(prog)
                        audio_bar.progress(100)
                        st.success("✅ Audio generated!")
                        audio_path = f"narration/narration_{idx}.mp3"
                        st.audio(audio_path)

                        # ===== Video Generation =====
                        st.markdown("**Step 3: Building Video...**")
                        video_bar = st.progress(0)
                        video_path = f"output/video_{idx}.mp4"
                        for stage, prog in build_video(title, narration_text, out_path=video_path):
                            if stage == "video":
                                video_bar.progress(prog)
                        video_bar.progress(100)
                        st.success(f"✅ Video generated: {video_path}")
                        st.video(video_path)
                        st.markdown("---")

    except Exception as e:
        st.error(f"Error parsing sheet URL or fetching data: {e}")
