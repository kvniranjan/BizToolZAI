import re

with open('/root/.openclaw/workspace/HEARTBEAT.md', 'r') as f:
    content = f.read()

# Update the Broke Economist section
new_section = """## ⏸️ PAUSED: The Broke Economist
- **Status:** Paused. The Kie.ai API issue has been identified and patched (the payload required an `input` key instead of `params`), but we are waiting for BOSS to give the green light before restarting the automated pipeline."""

content = re.sub(
    r'## ⏸️ PAUSED: The Broke Economist.*?(?=\n## 🔄)', 
    new_section + "\n", 
    content, 
    flags=re.DOTALL
)

with open('/root/.openclaw/workspace/HEARTBEAT.md', 'w') as f:
    f.write(content)
