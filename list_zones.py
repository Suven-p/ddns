import json
from urllib.request import Request, urlopen

with open("config.json") as f:
    config = json.load(f)
base_url = "https://api.cloudflare.com/client/v4"
headers = {
    "Authorization": "Bearer " + config["auth_key"],
    "Content-Type": "application/json",
}

url = f"{base_url}/zones"
request = Request(url, headers=headers)
with urlopen(request) as response:
    body = response.read().decode("utf-8")
response = json.loads(body)
if response["success"]:
    for zone in response["result"]:
        print(zone["name"], zone["id"])
