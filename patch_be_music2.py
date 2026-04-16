import re

file_path = '/root/.openclaw/workspace/broke_economist_daily_bytedance.py'
with open(file_path, 'r') as f:
    content = f.read()

old_ffmpeg = """log("4.5 Mixing Music...")
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
]
res = subprocess.run(cmd, capture_output=True, text=True)"""

new_ffmpeg = """log("4.5 Mixing Music...")
MUSIC_FILE = f"{WORKSPACE}/videos/audio/background_music.mp3"
audio_mix = f"{BE_DIR}/audio_mixed.mp3"

if os.path.exists(MUSIC_FILE):
    # Get exact audio duration
    duration_str = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path], capture_output=True, text=True).stdout.strip()
    total_duration = float(duration_str)
    
    music_temp = f"{BE_DIR}/music_temp.mp3"
    subprocess.run(["ffmpeg","-y","-i",MUSIC_FILE,
                   "-t", str(total_duration), "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={total_duration-3:.1f}:d=3,volume=0.15",
                   music_temp], capture_output=True)
                   
    subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_temp,
                   "-filter_complex","[0:a]volume=1.0[v];[1:a]volume=1.0[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",
                   "-map","[out]", audio_mix], capture_output=True)
else:
    log("Warning: background_music.mp3 not found. Rendering without music.")
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
]
res = subprocess.run(cmd, capture_output=True, text=True)"""

if old_ffmpeg in content:
    content = content.replace(old_ffmpeg, new_ffmpeg)
    with open(file_path, 'w') as f:
        f.write(content)
    print("Patched FFmpeg code successfully with actual background music.")
else:
    print("Could not find the exact FFmpeg block to patch. Please review.")
