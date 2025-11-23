# video_assembler.py
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Correct MoviePy imports for your current environment
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from src.tts_generator import generate_narration


VIDEO_W, VIDEO_H = 1280, 720
FPS = 30
def text_image_clip(title: str, body: str, duration: float = 25, bg_color=(30,30,50)) -> ImageClip:
    """Render a slide with title and body text."""
    import textwrap
    img = Image.new("RGB", (VIDEO_W, VIDEO_H), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 38)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Draw title
    tb = draw.textbbox((0,0), title, font=title_font)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    draw.text(((VIDEO_W-tw)//2, int(VIDEO_H*0.2)), title, font=title_font, fill="white")

    # Draw body text
    wrapped = textwrap.fill(body, width=55)
    bb = draw.multiline_textbbox((0,0), wrapped, font=body_font)
    bw, bh = bb[2]-bb[0], bb[3]-bb[1]
    draw.multiline_text(((VIDEO_W-bw)//2, int(VIDEO_H*0.5)), wrapped, font=body_font, fill="lightgrey", align="center")

    clip = ImageClip(np.array(img)).with_duration(duration)
    return clip

def build_video(title: str, description: str, out_path: str = "output.mp4", max_duration: float = 180) -> str:
    """
    Build a video from a script (title + description).
    """
    sentences = [s.strip() for s in description.split(".") if s.strip()]
    if len(sentences) < 7:
        while len(sentences) < 7:
            sentences.append(sentences[-1] if sentences else "Insight.")

    narr_audio_path = generate_narration(" ".join(sentences), "narration/narration_full.mp3")
    narr_audio = AudioFileClip(narr_audio_path)

    total_duration = min(narr_audio.duration, max_duration)
    per_seg = total_duration / 7

    clips = []
    current_t = 0.0
    segment_titles = ["Hook", "Intro", "Details", "Examples", "Benefits", "Challenges", "Future"]

    for i in range(7):
        seg_dur = min(per_seg, narr_audio.duration - current_t)
        if seg_dur <= 0:
            break
        scene = text_image_clip(segment_titles[i], sentences[i], seg_dur)
        a_sub = narr_audio.subclipped(current_t, current_t + seg_dur)
        scene = scene.with_audio(a_sub)
        clips.append(scene)
        current_t += seg_dur

    final = concatenate_videoclips(clips, method="compose")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    final.write_videofile(out_path, fps=FPS, codec="libx264", audio_codec="aac")
    return out_path