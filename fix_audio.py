import requests, os, re

ELEVENLABS_KEY = "2430b417f4d4a39161a9164953d80c62ff4d5cf19734e73a9dba9094ac474949"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

# Clean script - no markdown, no asterisks, no special chars
script = """February 1959. Nine experienced Russian hikers venture into the frozen Dyatlov Pass. They never return.

Weeks later, search parties discover their camp abandoned. The tent slashed open from the inside. Their belongings left behind. Footprints lead into the deadly snow — some bare, some clad only in socks.

Two bodies found near a dying fire. Others scattered, partially clothed. Some with catastrophic internal injuries, yet no visible external wounds. One woman missing her tongue and eyes. Traces of radiation found on their clothing.

The official Soviet conclusion — a compelling unknown natural force.

Over sixty years later, the truth of Dyatlov Pass remains buried. What do you believe happened?"""

# Double-check: strip any remaining markdown symbols
script = re.sub(r'\*+', '', script)
script = re.sub(r'#+', '', script)
script = script.strip()

print("📝 Clean script preview:")
print(script[:200])
print("\n🎙️ Generating clean voiceover via ElevenLabs...")

r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
    headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
    json={
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.75}
    }
)

if r.status_code == 200:
    with open("videos/audio/voiceover_clean.mp3", "wb") as f:
        f.write(r.content)
    print("✅ Clean voiceover saved to videos/audio/voiceover_clean.mp3")
else:
    print("❌ Error:", r.text)
