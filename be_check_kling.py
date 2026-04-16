import os, requests, json
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")
headers_kie = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}

tasks = ["46aa83bdb3f0b649cc40c8e4c58f450a", "b50ea65f7460a629825e022a38fdc205", "0fa17d46eb9311cc711d00684970254d"]

for t in tasks:
    r = requests.get(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={t}", headers=headers_kie).json()
    state = r.get('data', {}).get('state', 'Unknown')
    print(f"Task {t}: {state}")
