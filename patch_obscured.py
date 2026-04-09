import sys
with open("/root/.openclaw/workspace/obscured_daily.py", "r") as f:
    content = f.read()

# Replace the gemini generation with a file check
replacement = """
import sys
if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
    log(f"📂 Loading custom script from {sys.argv[1]}")
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    date_str = sys.argv[1].split('/')[-1].replace('.json', '')
else:
    raw = gemini(research_prompt)
    raw = re.sub(r'```json\n?', '', raw).replace('```', '').strip()
    try:
        data = json.loads(raw)
    except:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        data = json.loads(match.group()) if match else None

    if not data:
        log("❌ Failed to parse script JSON")
        sys.exit(1)
    date_str = datetime.now().strftime("%Y-%m-%d")
"""

content = content.replace("""raw = gemini(research_prompt)
raw = re.sub(r'```json\n?', '', raw).replace('```', '').strip()

try:
    data = json.loads(raw)
except:
    # Try to extract JSON
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    data = json.loads(match.group()) if match else None

if not data:
    log("❌ Failed to parse script JSON")
    sys.exit(1)

log(f"✅ Topic: {data['title']}")
log(f"   Hook: {data['hook']}")

date_str = datetime.now().strftime("%Y-%m-%d")""", replacement + """
log(f"✅ Topic: {data['title']}")
log(f"   Hook: {data['hook']}")
""")

with open("/root/.openclaw/workspace/obscured_daily.py", "w") as f:
    f.write(content)
print("Patched obscured_daily.py")
