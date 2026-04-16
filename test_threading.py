import concurrent.futures
import time

def dummy_task(clip_id):
    time.sleep(1)
    return f"Clip {clip_id} generated."

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(dummy_task, range(1, 11)))
print("Queue test:", results)
