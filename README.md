# Dynamic DNS Updater

A custom script to dynamically update a DNS record on Cloudflare. In config.json, `auth_key` is cloudflare's API Token, `zone_id` is the zone id of the domain name. `IP` field is used to cache results from last run.

## Usage
- Clone the repo
  ```bash
  git clone https://github.com/Suven-p/ddns.git ~/ddns
  ```
- Create config.json where the repository is cloned and set auth_key and zone_id.
  ```bash
  cp ~/ddns/config_example.json ~/ddns/config.json
  ```
  To list available zones after setting auth_key use
  ```bash
  python list_zones.py
  ```
- Optionally, include `record_id` to update a specific record, otherwise the script will update the first record that matches the host name.
- Set system hostname to the domain name for which record is to be updated. Example:
  ```bash
  sudo hostnamectl set-hostname myvm.example.com
  ```
- Run or schedule script.sh to update the DNS record. Example crontab for updating every 5 minutes:
  ```bash
  */5 * * * * cd ~/ddns && bash ./script.sh >> ~/ddns/log.txt 2>~/ddns/log.err
  ```
  if repositiory is cloned to `~/ddns`.
