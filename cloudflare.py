from urllib import request
from urllib.request import urlopen, Request
import json


with open("config.json") as f:
    config = json.load(f)
host_name = config["host_name"]
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
        return (
            response["result"][0]["id"],
            response["result"][0]["content"],
        )


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
        print(f"DNS Record updated to {new_ip}.")
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
    old_ip = None
    if record_id is None:
        record_id, old_ip = get_record(zone_id, host_name)
    current_ip = get_current_ip()

    if current_ip == old_ip:
        print("IP address is same. No need to update.")
        exit(0)

    update_dns_record(zone_id, record_id, current_ip)
