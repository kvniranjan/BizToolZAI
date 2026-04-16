import requests

url = "https://kie.ai/market"
headers = {"User-Agent": "Mozilla/5.0"}
html = requests.get(url, headers=headers).text

# Try to find some model strings in the raw HTML
import re
models = re.findall(r'([a-z0-9-]+/[a-z0-9-]+)', html)
models = list(set([m for m in models if 'video' in m or 'image' in m]))
print("Found possible models:", models)
