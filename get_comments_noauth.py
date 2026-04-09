import json
import urllib.request
import re

url = "https://www.youtube.com/shorts/fVxaWNPpp_s"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    # Try to grab anything that looks like a comment from ytInitialData
    print("Fetched HTML successfully. length:", len(html))
    match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if match:
        data = json.loads(match.group(1))
        # Shorts comments are usually loaded asynchronously, so they won't be in initial data
        print("Initial data parsed, but comments likely load asynchronously.")
except Exception as e:
    print(e)
