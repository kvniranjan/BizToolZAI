import re

file_path = '/root/.openclaw/workspace/broke_economist_daily_bytedance.py'

with open(file_path, 'r') as f:
    content = f.read()

# Since we need to trigger the shorts feed, maybe the current music track is getting copyright claimed or suppressed
# Let's add a log line and see if we can use a known-good track or increase volume
# Actually, the quickest way to force seed views is injecting it into high-traffic platforms automatically.
# The user wants ruthless growth. We will auto-post to Twitter/X if we had credentials, but we only have Reddit.

# Let's refine the ffmpeg command to make the video even more engaging: add a very slight zoom/pan effect to the video.
old_ffmpeg = """cmd = [
    "ffmpeg", "-y", 
    "-i", concat_vid, 
    "-i", audio_mix,
    "-vf", f"subtitles={srt_path}:force_style='FontName=Impact,FontSize=24,Bold=1,PrimaryColour=&H0000D7FF,OutlineColour=&H00000000,Outline=4,Shadow=3,Alignment=2,MarginV=180'",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac",
    "-shortest", final_vid
]"""

# Add a subtle zoom-in effect over the 45 seconds to keep the eye moving, which increases retention.
new_ffmpeg = """cmd = [
    "ffmpeg", "-y", 
    "-i", concat_vid, 
    "-i", audio_mix,
    "-vf", f"zoompan=z='min(zoom+0.0005,1.1)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',subtitles={srt_path}:force_style='FontName=Impact,FontSize=24,Bold=1,PrimaryColour=&H0000D7FF,OutlineColour=&H00000000,Outline=4,Shadow=3,Alignment=2,MarginV=180'",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac",
    "-shortest", final_vid
]"""

content = content.replace(old_ffmpeg, new_ffmpeg)

with open(file_path, 'w') as f:
    f.write(content)

print("Added zoompan effect for visual retention.")
