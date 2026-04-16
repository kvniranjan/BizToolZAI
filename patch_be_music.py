file_path = '/root/.openclaw/workspace/be_pipeline_v4_bytedance.py'
with open(file_path, 'r') as f:
    content = f.read()

old_ffmpeg = """final_vid = f"{BE_DIR}/final.mp4"
cmd = [
    "ffmpeg", "-y", 
    "-i", concat_vid, 
    "-i", audio_path,
    "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=20,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=3,Shadow=2,Alignment=2,MarginV=100'",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac",
    "-shortest", final_vid
]"""

new_ffmpeg = """
log("4.5 Mixing Music...")
MUSIC_FILE = f"{WORKSPACE}/Charlie.mp3"  # Standard aggressive/suspenseful track we have lying around
audio_mix = f"{BE_DIR}/audio_mixed.mp3"
if os.path.exists(MUSIC_FILE):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", audio_path,
        "-i", MUSIC_FILE,
        "-filter_complex", "[0:a]volume=1.2[a1];[1:a]volume=0.15[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]", audio_mix
    ], capture_output=True, check=True)
else:
    log("Warning: Charlie.mp3 not found. Rendering without music.")
    audio_mix = audio_path

final_vid = f"{BE_DIR}/final.mp4"
cmd = [
    "ffmpeg", "-y", 
    "-i", concat_vid, 
    "-i", audio_mix,
    "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=20,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=3,Shadow=2,Alignment=2,MarginV=100'",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac",
    "-shortest", final_vid
]"""

if old_ffmpeg in content:
    content = content.replace(old_ffmpeg, new_ffmpeg)
    with open(file_path, 'w') as f:
        f.write(content)
    print("Patched FFmpeg code successfully with music mixing.")
else:
    print("Could not find the exact FFmpeg block to patch. Please review.")
