import json
import time

try:
    with open('/root/.openclaw/workspace/memory/heartbeat-state.json', 'r') as f:
        data = json.load(f)
except Exception:
    data = {"lastChecks": {}}

now = int(time.time())
data["lastChecks"]["youtube"] = now
data["lastChecks"]["signals"] = now

with open('/root/.openclaw/workspace/memory/heartbeat-state.json', 'w') as f:
    json.dump(data, f, indent=2)
