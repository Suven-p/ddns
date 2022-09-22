# Dynamic DNS Updater

A custom script to dynamically update a DNS record on Cloudflare. In config.json, `auth_key` is cloudflare's API Token, `host_name` is the domain name, `zone_id` is the zone id of the domain name. Optionally, include `record_id` to update a specific record, otherwise the script will update the first record that matches the host name. Run or schedule script.sh to update the DNS record.
Use
```bash
python list_zones.py
```
to list available zones.
