import json, os, subprocess

scripts = [
    {
        "title": "The Ghost Ship of 1872 #Shorts",
        "hook": "A ship drifting aimlessly. The crew vanished. Breakfast still warm.",
        "voiceover": "In 1872, the Mary Celeste was found drifting in the middle of the Atlantic. There were no signs of a struggle. Six months of food and water sat untouched. The crew's personal belongings were still folded in their cabins. But all ten people on board were gone, never to be seen again. The lifeboats were missing, but the ship was completely seaworthy. What made them abandon a perfectly safe vessel into the unforgiving ocean? I'm about to tell you the scariest part, but first, hit subscribe so you don't miss tomorrow's mystery. The final entry in the captain's log gave absolutely no indication of danger. They just walked off the ship.",
        "image_prompts": [
            "Cinematic ultra-realistic dark atmospheric historical photo of an abandoned 1800s wooden ship drifting in thick ocean fog, moody lighting, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of an untouched warm breakfast on a wooden ship table, no people, eerie, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of a creepy empty wooden ship cabin, belongings folded neatly, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of an empty captain's desk with an open logbook, dark lighting, 9:16 vertical"
        ],
        "description": "What really happened to the Mary Celeste? An entire crew vanished, leaving everything behind. #ObscuredHistory #Mystery #DarkHistory #Shorts #Unsolved",
        "tags": ["ObscuredHistory", "UnsolvedMystery", "DarkHistory", "TrueHistory", "Shorts", "MaryCeleste", "GhostShip"]
    },
    {
        "title": "115 People Vanished Overnight #Shorts",
        "hook": "An entire colony vanished without a trace. Just one word remained.",
        "voiceover": "In 1590, a governor returned to the Roanoke colony with fresh supplies. But he found the settlement completely abandoned. There were no bodies, and no signs of a struggle. The houses had been carefully taken down, meaning they didn't flee in a panic. The only clue to where 115 men, women, and children went? The word CROATOAN carved into a wooden post. Over 400 years later, we still have absolutely no idea what took them. I'm about to tell you the scariest part, but first, hit subscribe so you don't miss tomorrow's mystery. The local tribes reported no strange activity, and no bodies were ever recovered.",
        "image_prompts": [
            "Cinematic ultra-realistic dark atmospheric historical photo of an empty 1500s colonial settlement, dirt roads, eerie fog, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of colonial houses being systematically taken down, empty village, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of the word CROATOAN carved into a creepy old wooden tree post, dark lighting, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of a dark, scary forest edge surrounding an empty 1500s village, 9:16 vertical"
        ],
        "description": "Where did the Roanoke colony go? 115 people disappeared without a trace. #ObscuredHistory #Mystery #DarkHistory #Shorts #Unsolved",
        "tags": ["ObscuredHistory", "UnsolvedMystery", "DarkHistory", "TrueHistory", "Shorts", "Roanoke", "LostColony"]
    },
    {
        "title": "The Shipwreck With Warm Food #Shorts",
        "hook": "A massive ship crashed ashore. Ribs cooking. But no crew.",
        "voiceover": "In 1921, the Carroll A. Deering washed up on the shores of North Carolina. When the Coast Guard finally boarded the massive vessel, they found ribs actively boiling on the galley stove. But the crew's logs, their lifeboats, and all ten men had completely vanished. No distress call was ever sent. The ship's steering wheel was shattered, yet everything else was pristine. Where did they go? I'm about to tell you the scariest part, but first, hit subscribe so you don't miss tomorrow's mystery. Messages in bottles claiming they were captured by pirates washed up years later, but their authenticity remains unsolved.",
        "image_prompts": [
            "Cinematic ultra-realistic dark atmospheric historical photo of a massive 1920s ship washed ashore on a stormy beach at dusk, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of an empty ship galley with a pot boiling on a stove, eerie, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of a shattered wooden steering wheel on a ship deck, dark lighting, 9:16 vertical",
            "Cinematic ultra-realistic dark atmospheric historical photo of an old glass bottle washing up on a dark spooky beach, 9:16 vertical"
        ],
        "description": "The Carroll A. Deering is one of history's creepiest ghost ships. Where did the crew go? #ObscuredHistory #Mystery #DarkHistory #Shorts #Unsolved",
        "tags": ["ObscuredHistory", "UnsolvedMystery", "DarkHistory", "TrueHistory", "Shorts", "GhostShip", "Shipwreck"]
    }
]

import string
import random

def patch_and_run(script_data, index):
    file_id = f"custom_run_{index}"
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
    wrapper_path = f"/root/.openclaw/workspace/run_wrapper_{index}.py"
    with open(wrapper_path, "w") as f:
        f.write(wrapper)
        
    print(f"Running {file_id}...")
    subprocess.run(["/root/.openclaw/workspace/venv/bin/python3", wrapper_path])
    
for i, s in enumerate(scripts):
    patch_and_run(s, i)

