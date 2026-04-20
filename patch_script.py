import re

with open('/root/.openclaw/workspace/obscured_daily.py', 'r') as f:
    code = f.read()

# Upgrade ElevenLabs Model
code = code.replace('"model_id": "eleven_monolingual_v1"', '"model_id": "eleven_turbo_v2_5"')

# Upgrade Captions (Bigger, Impact Font, Yellow, Higher Margin)
code = code.replace(
    "FontName=Arial,FontSize=18,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=60",
    "FontName=Impact,FontSize=24,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=3,Shadow=2,Alignment=2,MarginV=80"
)

# Speed up the Ken Burns effect for better retention
code = code.replace(
    "zoompan=z='min(zoom+0.0004,1.12)'",
    "zoompan=z='min(zoom+0.0008,1.25)'"
)

# Improve Prompt for more aggressive hooks
code = code.replace(
    "1. HOOK (0-3s): Shocking statement that creates an open loop",
    "1. HOOK (0-3s): Paced visually. Start with rapid 2-4 word phrases. Shocking statement that creates an instant open loop. DO NOT start with 'In [year]'."
)

# Make the pinned comment more aggressive for engagement/subs
code = code.replace(
    "f\"This one genuinely unsettles me. What do you think really happened? 👇\",",
    "f\"This one genuinely unsettles me. If you made it this far, hit SUBSCRIBE for daily mysteries. What do you think really happened? 👇\","
)
code = code.replace(
    "f\"The more you research this, the stranger it gets. Drop your theory below 👇\",",
    "f\"The more you research this, the stranger it gets. SUBSCRIBE to uncover more lost history. Drop your theory below 👇\","
)

with open('/root/.openclaw/workspace/obscured_daily.py', 'w') as f:
    f.write(code)

print("Patch applied!")
