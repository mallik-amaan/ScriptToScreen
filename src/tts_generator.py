# src/tts_generator.py
from gtts import gTTS
import os
import tempfile

def generate_narration(text: str, out_path: str):
    """
    Generates TTS audio and returns path. Yields progress percentage for Streamlit.
    """
    # Split text into chunks for progress tracking
    sentences = text.split(". ")
    total = len(sentences)
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        temp_path = tmp_file.name
    
    for idx, sentence in enumerate(sentences, 1):
        tts = gTTS(sentence)
        tmp_audio = f"{temp_path}_{idx}.mp3"
        tts.save(tmp_audio)
        # Append to final file
        os.system(f'ffmpeg -y -i "concat:{tmp_audio}" -acodec copy "{out_path}"')
        progress = int((idx / total) * 100)
        yield progress  # Streamlit can update progress bar
