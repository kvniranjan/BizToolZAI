import re

file_path = '/root/.openclaw/workspace/broke_economist_daily_bytedance.py'

with open(file_path, 'r') as f:
    content = f.read()

# 1. Dynamic Trending Topic Generation instead of a static list
old_topic_block = """import datetime
# Select a random topic from a predefined list so it doesn't repeat
import random
topics = [
    "Why your savings account is a scam",
    "The truth about credit scores",
    "How billionaires actually buy mega yachts",
    "Why rent will never go down",
    "The dirty secret behind 0% financing",
    "Why college degrees are depreciating assets",
    "How inflation is a stealth tax",
    "The reason your car insurance is skyrocketing",
    "Why you should never 'buy now, pay later'",
    "The illusion of free shipping"
]
selected_topic = random.choice(topics)
log(f"Topic chosen: {selected_topic}")

prompt = f\"\"\"You are 'The Broke Economist'. Write a 45-second YouTube Short script about '{selected_topic}'.
Tone: cynical, dark humor, exposing the game, aggressive pacing but sarcastic.
Format the output EXACTLY as valid JSON with no markdown formatting:
{{
  "title": "A highly clickable YouTube Shorts title (under 50 chars)",
  "hook": "The first 3 seconds...",
  "voiceover": "The full voiceover text including the hook. No asterisks, no sound effect notes.",
  "prompts": [
    "A cinematic animated shot of...",
    "A cinematic animated shot of...",
    "A cinematic animated shot of..."
  ]
}}
Provide EXACTLY 3 prompts. Make them highly cinematic, dynamic camera movements for Bytedance Seedance Video Generation. Ensure prompts are 9:16 aspect ratio suitable.\"\"\""""

new_topic_block = """import datetime
import random

# Generate a high-retention, controversial, or trend-jacking topic dynamically
topic_prompt = \"\"\"You are a viral YouTube Shorts strategist for a finance channel called 'The Broke Economist'. 
Generate 1 highly controversial, contrarian, or cynical finance topic that exposes a 'scam' or hidden truth about money, real estate, investing, or corporate greed. It must be highly relatable to broke millennials/Gen Z.
Output ONLY the topic sentence, nothing else. Examples: 'Why your 401k is a trap designed to keep you working', 'The dark psychology of grocery store layouts', 'Why Dave Ramsey's advice is keeping you poor'.\"\"\"

topic_resp = model.generate_content(topic_prompt)
selected_topic = topic_resp.text.strip().strip('"')
log(f"Dynamic Topic chosen: {selected_topic}")

prompt = f\"\"\"You are 'The Broke Economist'. Write a fast-paced, highly engaging 45-second YouTube Short script about: '{selected_topic}'.
Tone: cynical, dark humor, exposing the game, aggressive pacing. Hook the viewer in the first 2 seconds with a controversial statement.
Use short, punchy sentences. High energy.

Format the output EXACTLY as valid JSON with no markdown formatting:
{{
  "title": "A viral, clickbaity YouTube Shorts title (under 50 chars)",
  "seo_tags": ["finance", "tag2", "tag3", "tag4", "tag5"],
  "hook": "The first 3 seconds (must be controversial/curiosity-inducing)...",
  "voiceover": "The full voiceover text including the hook. No asterisks, no sound effect notes.",
  "prompts": [
    "A cinematic animated shot of...",
    "A cinematic animated shot of...",
    "A cinematic animated shot of..."
  ]
}}
Provide EXACTLY 3 prompts. Make them highly cinematic, dynamic camera movements, photorealistic, 9:16 aspect ratio.\"\"\""""

content = content.replace(old_topic_block, new_topic_block)

# 2. Upgrade the FFMPEG Subtitles (Hormozi style - larger, bold yellow, black outline)
old_ffmpeg = """cmd = [
    "ffmpeg", "-y", 
    "-i", concat_vid, 
    "-i", audio_mix,
    "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=20,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=3,Shadow=2,Alignment=2,MarginV=100'",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac",
    "-shortest", final_vid
]"""

# Yellow text, thick black border, centered slightly higher, larger font
new_ffmpeg = """cmd = [
    "ffmpeg", "-y", 
    "-i", concat_vid, 
    "-i", audio_mix,
    "-vf", f"subtitles={srt_path}:force_style='FontName=Impact,FontSize=24,Bold=1,PrimaryColour=&H0000D7FF,OutlineColour=&H00000000,Outline=4,Shadow=3,Alignment=2,MarginV=180'",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac",
    "-shortest", final_vid
]"""

content = content.replace(old_ffmpeg, new_ffmpeg)

# 3. Inject Dynamic SEO Tags into YouTube Upload
old_yt_tags = """        "description": f"{data.get('hook', '')}\\n\\n#finance #economics #money",
        "tags": ["finance", "economics", "money", "wealth"],"""

new_yt_tags = """        "description": f"{data.get('hook', '')}\\n\\n#finance #economics #money #investing #wealth",
        "tags": data.get('seo_tags', ["finance", "economics", "money", "wealth"]),"""

content = content.replace(old_yt_tags, new_yt_tags)

with open(file_path, 'w') as f:
    f.write(content)

print("Patch applied successfully.")
