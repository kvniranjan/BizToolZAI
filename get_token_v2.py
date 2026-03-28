import requests, json, pickle
from google.oauth2.credentials import Credentials

# Exchange using direct HTTP request (bypasses PKCE issue)
CLIENT_ID = "342216342764-bhb41va8mksn1bdg6hjn12n9spu53oef.apps.googleusercontent.com"
CLIENT_SECRET = "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"
CODE = "4/1Aci98E_UHtyTSvG8gqauWzp25FHubT3dk-Bta7O6j_dMMps_IabOjTmD0pM"

r = requests.post("https://oauth2.googleapis.com/token", data={
    "code": CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "grant_type": "authorization_code"
})

print("Status:", r.status_code)
print("Response:", r.text[:500])
