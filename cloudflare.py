from datetime import datetime
import json
from urllib.request import urlopen, Request
import socket

forced = False
with open("config.json") as f:
    config = json.load(f)
host_name = socket.gethostname()
zone_id = config["zone_id"]
base_url = "https://api.cloudflare.com/client/v4"
headers = {
    "Authorization": "Bearer " + config["auth_key"],
    "Content-Type": "application/json",
}


def get_current_ip():
    with urlopen("https://api.ipify.org") as response:
        body = response.read().decode("utf-8")
    return body


def get_record(zone_id, record_name):
    url = f"{base_url}/zones/{zone_id}/dns_records?name={record_name}"
    request = Request(url, headers=headers)
    with urlopen(request) as response:
        body = response.read().decode("utf-8")
    response = json.loads(body)
    if response["success"]:
        return response["result"][0]["id"]


def update_dns_record(zone_id, record_id, record_content):
    url = f"{base_url}/zones/{zone_id}/dns_records/{record_id}"
    data = {"content": record_content}
    request = Request(
        url, headers=headers, data=json.dumps(data).encode("utf-8"), method="PATCH"
    )
    with urlopen(request) as response:
        body = response.read().decode("utf-8")
    response = json.loads(body)
    new_ip = response["result"]["content"]
    if response["success"]:
        print(f"DNS Record updated to {new_ip} at {datetime.now()}.")
    return new_ip


def create_dns_record(zone_id, record_name, record_content):
    url = f"{base_url}/zones/{zone_id}/dns_records"
    data = {
        "type": "A",
        "name": record_name,
        "content": record_content,
        "ttl": 1,
        "proxied": False,
    }
    request = Request(
        url, headers=headers, data=json.dumps(data).encode("utf-8"), method="POST"
    )
    with urlopen(request) as response:
        body = response.read().decode("utf-8")
    response = json.loads(body)
    if response["success"]:
        print(f"DNS Record created with IP {record_content}.")
    return response["result"]["content"]


if __name__ == "__main__":
    record_id = config.get("record_id", None)
    stored_ip = config.get("IP", None)
    current_ip = get_current_ip()
    if stored_ip == current_ip and not forced:
        print(f"IP address is same at {datetime.now()}. No need to update")
        exit(0)

    if record_id is None:
        record_id = get_record(zone_id, host_name)

    new_ip = update_dns_record(zone_id, record_id, current_ip)
    config["IP"] = new_ip
    with open("config.json", "w") as f:
        json.dump(config, f)
