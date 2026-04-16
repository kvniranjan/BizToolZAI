import time, os
from datetime import datetime

log_file = "/root/.openclaw/workspace/be_v2.log"
print(f"Monitoring {log_file} for completion...")

def get_last_lines():
    try:
        with open(log_file, "r") as f:
            return f.readlines()[-5:]
    except:
        return []

last_check = get_last_lines()

# Just run a quick check, don't block
if any("5. Stitching Video..." in line for line in last_check):
    print("Stitching has started!")
elif any("V2 Pipeline Render Complete" in line for line in last_check):
    print("Render Complete!")
else:
    print("Still polling...")
