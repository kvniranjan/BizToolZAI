import sys, json, requests
from oauthlib.oauth2 import WebApplicationClient

with open("client_secret_drive.json", "r") as f:
    creds = json.load(f)["installed"]

client_id = creds["client_id"]
client_secret = creds["client_secret"]
token_url = creds["token_uri"]

code = sys.argv[1]
client = WebApplicationClient(client_id)
token_request = client.prepare_request_body(
    code=code,
    redirect_uri="http://localhost",
    client_secret=client_secret
)

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(token_url, data=token_request, headers=headers)
token_data = response.json()

token_data["client_id"] = client_id
token_data["client_secret"] = client_secret
token_data["token_uri"] = token_url
token_data["scopes"] = ["https://www.googleapis.com/auth/drive.file"]

with open("drive_token.json", "w") as f:
    json.dump(token_data, f)
print("Drive token saved!")
