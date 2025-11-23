# main.py
import streamlit as st
import os
import time
import traceback
from urllib.parse import urlparse, parse_qs

from src.sheet_reader import read_sheet
from src.script_generator import generate_script, setup_genai
from src.tts_generator import generate_narration
from src.video_assembler import build_video


st.set_page_config(page_title="Script2Screen", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4B0082;'>Script2Screen: Generate Video from Google Sheets</h1>", unsafe_allow_html=True)
st.markdown("---")


# ----------------------------
# 1️⃣ Input Google Sheet URL
# ----------------------------
sheet_url = st.text_input(
    "Enter your Google Sheet URL",
    "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0"
)

if sheet_url:
    try:
        # Extract Sheet ID
        parsed = urlparse(sheet_url)

        if "/d/" in parsed.path:
            sheet_id = parsed.path.split("/d/")[1].split("/")[0]
        else:
            qs = parse_qs(parsed.query)
            sheet_id = qs.get("id", [None])[0]

        if not sheet_id:
            st.error("Could not extract Sheet ID. Please check the URL.")
            st.stop()

        st.success(f"Extracted Sheet ID: {sheet_id}")
        st.info("⚠️ Share your Google Sheet with the service account email below (Edit access required):")
        st.code(os.getenv("SERVICE_EMAIL"))


        st.markdown("<h3 style='text-align: center;'>Step 1: Generate Videos</h3>", unsafe_allow_html=True)


        # ----------------------------
        # 2️⃣ Start Processing
        # ----------------------------
        if st.button("Generate Videos", key="gen_videos"):

            setup_genai()
            st.info("Fetching sheet data...")

            df, records_gen = read_sheet(
                sheet_id=sheet_id,
                sheet_name="Sheet1",
                data_range="A1:B11"
            )

            # Convert generator → list
            records = list(records_gen)

            st.success("Sheet data fetched successfully!")
            st.dataframe(df.head())

            # ----------------------------
            # 3️⃣ Loop through each row
            # ----------------------------
            for idx, entry in enumerate(records):

                title = entry["Title"]
                description = entry["Description"]

                st.markdown(f"<h3 style='color:#4B0082;'>Processing: {title}</h3>", unsafe_allow_html=True)

                # ----------------------------
                # Step 1: Script Generation
                # ----------------------------
                st.markdown("**Generating script...**")
                script_progress = st.progress(0)

                for i in range(0, 101, 20):
                    time.sleep(0.1)
                    script_progress.progress(i)

                script_data = generate_script(title, description)
                narration_text = script_data.get("script", description)

                st.success("✅ Script generated!")


                # ----------------------------
                # Step 2: Audio Generation
                # ----------------------------
                st.markdown("**Generating narration audio...**")
                audio_progress = st.progress(0)

                for i in range(0, 101, 25):
                    time.sleep(0.1)
                    audio_progress.progress(i)

                audio_path = generate_narration(
                    narration_text,
                    f"narration/narration_{idx}.mp3"
                )

                # DEBUG
                st.write("DEBUG: audio_path type →", str(type(audio_path)))

                if not isinstance(audio_path, str):
                    st.error(f"❌ generate_narration() returned invalid type: {type(audio_path)}")
                    st.stop()

                st.success("✅ Audio generated!")
                st.audio(audio_path)


                # ----------------------------
                # Step 3: Video Generation
                # ----------------------------
                st.markdown("**Generating video...**")
                video_progress = st.progress(0)

                for i in range(0, 101, 20):
                    time.sleep(0.1)
                    video_progress.progress(i)

                video_path = build_video(
                    title=title,
                    description=narration_text,
                    out_path=f"output/video_{idx}.mp4",
                    max_duration=180
                )

                st.success(f"✅ Video generated: {video_path}")
                st.video(video_path)

                st.markdown("---")


    # ----------------------------
    # Global Exception Catcher
    # ----------------------------
    except Exception as e:
        st.error("❌ Error parsing sheet data or generating output!")
        st.exception(e)

        # Show full traceback text
        traceback_str = traceback.format_exc()
        st.text(traceback_str)
