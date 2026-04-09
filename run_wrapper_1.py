
import sys
import json
import builtins

original_open = builtins.open

with original_open('/root/.openclaw/workspace/obscured_daily.py', 'r') as f:
    code = f.read()

code = code.replace('datetime.now().strftime("%Y-%m-%d")', '"custom_run_1"')

inject = '''
import json
with open("/root/.openclaw/workspace/videos/custom_run_1.json", "r") as f:
    data = json.load(f)
raw = json.dumps(data)
'''

code = code.replace('raw = gemini(research_prompt)', inject)

exec(code, globals())
