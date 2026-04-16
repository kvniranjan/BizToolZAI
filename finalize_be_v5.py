import re

file_path = '/root/.openclaw/workspace/be_pipeline_v4_bytedance.py'
with open(file_path, 'r') as f:
    content = f.read()

# Swap the script generation prompt out of the hardcoded "Why Coffee Costs $8" test 
# and make it dynamic for daily cron use.
old_gen = """prompt = \"\"\"You are 'The Broke Economist'. Write a 45-second YouTube Short script about 'Why Coffee Costs $8 Now'.
Tone: cynical, dark humor, exposing the game, aggressive pacing but sarcastic.
Format the output EXACTLY as valid JSON with no markdown formatting:
{
  "hook": "The first 3 seconds...",
  "voiceover": "The full voiceover text including the hook. No asterisks, no sound effect notes.",
  "prompts": [
    "A cinematic animated shot of a sad millennial paying for coffee with a gold bar, dark moody lighting",
    "A cinematic animated shot of a giant corporate coffee cup crushing a small wallet, dark studio lighting",
    "A cinematic animated shot of a yacht made entirely out of coffee beans, hyperrealistic"
  ]
}
Provide EXACTLY 3 prompts. Make them highly cinematic, dynamic camera movements for Bytedance Seedance Video Generation.\"\"\""""

new_gen = """
import datetime
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
Provide EXACTLY 3 prompts. Make them highly cinematic, dynamic camera movements for Bytedance Seedance Video Generation. Ensure prompts are 9:16 aspect ratio suitable.\"\"\"
"""

content = content.replace(old_gen, new_gen)

# Also rename the script file to a daily script
new_name = "/root/.openclaw/workspace/broke_economist_daily_bytedance.py"
with open(new_name, 'w') as f:
    f.write(content)
print(f"Created {new_name}")
