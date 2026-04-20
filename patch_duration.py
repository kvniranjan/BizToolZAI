import re

with open('/root/.openclaw/workspace/obscured_daily.py', 'r') as f:
    code = f.read()

# Make sure duration doesn't exceed 59s
duration_fix = """
duration = float(res.stdout.strip())
log(f"✅ Voiceover: {duration:.1f}s")

if duration > 59.0:
    log("⚠️ Voiceover > 59s, applying atempo filter to fit Shorts format...")
    ratio = duration / 58.5
    speed_audio = f"{WORKSPACE}/videos/audio/vo_fast_{date_str}.mp3"
    subprocess.run(["ffmpeg", "-y", "-i", audio_path, "-filter:a", f"atempo={ratio}", speed_audio], capture_output=True)
    audio_path = speed_audio
    duration = 58.5
    log(f"✅ Voiceover sped up to 58.5s")
"""

code = code.replace(
    'duration = float(res.stdout.strip())\nlog(f"✅ Voiceover: {duration:.1f}s")',
    duration_fix
)

with open('/root/.openclaw/workspace/obscured_daily.py', 'w') as f:
    f.write(code)

print("Duration patch applied!")
