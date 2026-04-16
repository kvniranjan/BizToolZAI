import json
with open("drive_token.json", "r") as f:
    data = json.load(f)
if "access_token" in data:
    data["token"] = data["access_token"]
with open("drive_token.json", "w") as f:
    json.dump(data, f)
