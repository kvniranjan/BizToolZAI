import json, os, subprocess

scripts = [
    {
        "title": "The Bloody Doctor's Bag #Shorts",
        "hook": "A ship drifts aimlessly. 25 people vanished. On the deck? Bloody bandages.",
        "voiceover": "In 1955, the MV Joyita was found drifting in the South Pacific. All 25 passengers and crew were gone. But unlike other ghost ships, this wasn't peaceful. The radio was tuned to the universal distress channel. A doctor's bag lay on the deck, surrounded by bloody bandages. The ship was practically unsinkable, so why did they abandon it? I'm about to tell you the scariest part, but first, hit subscribe. The ship's logbook was completely missing, but the clocks had all stopped at exactly 10:25.",
        "image_prompts": [
            "Cinematic ultra-realistic photo of a 1950s 70-foot wooden twin-screw motor vessel drifting in the ocean, dark atmospheric, 9:16 vertical",
            "Cinematic ultra-realistic photo of an old 1950s leather doctor's bag on a wooden ship deck, bloody bandages around it, spooky lighting, 9:16 vertical",
            "Cinematic ultra-realistic photo of an empty ship radio room, vintage 1950s radio glowing in the dark, 9:16 vertical",
            "Cinematic ultra-realistic photo of a vintage wall clock on a ship stopped exactly at 10:25, eerie, 9:16 vertical"
        ],
        "description": "What happened on the MV Joyita? 25 people vanished, leaving behind a bloody scene. #ObscuredHistory #Mystery #DarkHistory #Shorts #Unsolved",
        "tags": ["ObscuredHistory", "UnsolvedMystery", "DarkHistory", "TrueHistory", "Shorts", "MVJoyita", "GhostShip"]
    },
    {
        "title": "The Kaz II Mystery #Shorts",
        "hook": "A yacht drifting at sea. Engine running. Laptop open. Everyone gone.",
        "voiceover": "In 2007, the Kaz II was discovered drifting off the coast of Australia. When authorities boarded, the engine was still running. A laptop was open and powered on. Food was set out on the table, and the life jackets were perfectly stowed. But the three men aboard were completely gone. There was no sign of a struggle, and the weather had been perfect. I'm about to tell you the scariest part, but first, hit subscribe. A video recovered from a camera on board showed them perfectly happy and relaxed just hours before they disappeared into thin air.",
        "image_prompts": [
            "Cinematic ultra-realistic photo of a modern 2007 white 9.8-meter catamaran yacht drifting on calm ocean water, eerie atmosphere, 9:16 vertical",
            "Cinematic ultra-realistic photo of a 2007 era silver laptop open and powered on sitting on a yacht table, nobody around, 9:16 vertical",
            "Cinematic ultra-realistic photo of an empty yacht deck with perfectly stowed life jackets, calm but spooky, 9:16 vertical",
            "Cinematic ultra-realistic photo of a digital camera resting on a yacht table showing an empty sea, 9:16 vertical"
        ],
        "description": "The Kaz II is a modern ghost ship. What happened to the three men on board? #ObscuredHistory #Mystery #DarkHistory #Shorts #Unsolved",
        "tags": ["ObscuredHistory", "UnsolvedMystery", "DarkHistory", "TrueHistory", "Shorts", "KazII", "GhostShip"]
    }
]

import string
import random

def patch_and_run(script_data, index):
    # Offset by 3 to avoid overwriting custom_run_0, 1, 2
    actual_index = index + 3 
    file_id = f"custom_run_{actual_index}"
    json_path = f"/root/.openclaw/workspace/videos/{file_id}.json"
    with open(json_path, "w") as f:
        json.dump(script_data, f)
    
    wrapper = f"""
import sys
import json
import builtins

original_open = builtins.open

with original_open('/root/.openclaw/workspace/obscured_daily.py', 'r') as f:
    code = f.read()

code = code.replace('datetime.now().strftime("%Y-%m-%d")', '"{file_id}"')

inject = '''
import json
with open("{json_path}", "r") as f:
    data = json.load(f)
raw = json.dumps(data)
'''

code = code.replace('raw = gemini(research_prompt)', inject)

exec(code, globals())
"""
    wrapper_path = f"/root/.openclaw/workspace/run_wrapper_{actual_index}.py"
    with open(wrapper_path, "w") as f:
        f.write(wrapper)
        
    print(f"Running {file_id}...")
    subprocess.run(["/root/.openclaw/workspace/venv/bin/python3", wrapper_path])
    
for i, s in enumerate(scripts):
    patch_and_run(s, i)