# Cloudflare-Dynamic-DNS
[![Python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![AM](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/CloudFlare-Dynamic-DNS)
[![Size](https://img.shields.io/github/repo-size/Suzhou65/CloudFlare-Dynamic-DNS.svg)](https://shields.io/category/size)

Small python script for request & update DNS Record hosting by Cloudflare via Cloudflare API.

## Contents
- [Cloudflare-Dynamic-DNS](#cloudflare-dynamic-dns)
  * [Contents](#contents)
  * [Usage](#usage)
    + [Scheduling](#scheduling)
    + [Cloudflare API](#cloudflare-api)
    + [Configuration file](#configuration-file)
    + [Error handling](#error-handling)
    + [Telegram alert](#telegram-alert)
  * [Import module](#import-module)
  * [Script](#script)
    + [Verify Cloudflare API Token](#verify-cloudflare-api-token)
    + [Request all DNS records](#request-all-dns-records)
    + [Request A record](#request-a-record)
    + [Request AAAA record](#request-aaaa-record)
    + [Update A record](#update-a-record)
    + [Update AAAA record](#update-aaaa-record)
    + [Update CNAME](#update-cname-record)
  * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module-1)
  * [License](#license)
  * [Resources](#resources)
    + [My GitHub Gist](#my-github-gist)
    + [Cloudflare API](#cloudflare-api-1)
    + [IP address request API](#ip-address-request-api)

## Usage
### Scheduling
- Crontab
Using Crontab for job scheduling.
```shell
#MIM HOUR DAY MONTH WEEK
*/30  *    *    *    *    root  python /script_path/script_ddns4.py
```
- Schedule
Alternatively, automatically execute via ```schedule``` module, scheduling examples as following.  
```python
import schedule
import sys

def SomethingAsPackage():
    # Please packing script as script

# Execute setting
schedule.every(30).minutes.do(SomethingAsPackage)
# Loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
# Manuel exit
except KeyboardInterrupt:
  sys.exit()
```
### Cloudflare API
```diff
- For safety reason, please using API Token instead of legacy API Keys.
```
For using module and script, you may need a domain registered with Cloudflare, or choice Cloudflare as DNS hosting service.

Then, logged into ```Cloudflare Dashboard```, select the domain you hosting, find the ```Get your API token``` banner, click [API Tokens](https://dash.cloudflare.com/profile/api-tokens) options.

Modify the token’s permissions. only allowing DNS record edit, then generate API Token. ```The token secret is only shown once, make sure to copy the secret to a secure place.```
### Configuration file
Cloudflare API Token, Zone ID, DNS records ID will storage at configuration file as JSON format, the standard configuration file structure as follows:
```json
{
   "Telegram_BOTs":{
      "TelegramToken": "",
      "TelegramChatID": ""
   },
   "CloudflareAPI":{
      "AuthToken": "",
      "AuthMail": ""
   },
  "Zone":{
      "ZoneID": ""
   },
  "RecordsID":{
      "DNSRecordIPv4ID": "",
      "DNSRecordIPv4Domain": "",
      "DNSRecordIPv4ProxyAble": true,
      "DNSRecordIPv4ProxyMode": true,
      "DNSRecordIPv6ID": "",
      "DNSRecordIPv6Domain": "",
      "DNSRecordIPv6ProxyAble": true,
      "DNSRecordIPv6ProxyMode": true
   },
   "IPAddressUpdateRecord": {
      "DNSRecordIPv4": "",
      "DNSRecordIPv4UpdateTime": "",
      "DNSRecordIPv6": "",
      "DNSRecordIPv6UpdateTime": ""
  },
  "CNAME": {
      "DNSRecordCNAMEID": "",
      "NAME": "",
      "TARGET": "",
      "DNSRecordCNAMEUpdateTime": ""
   }
}
```
For using configuration file, please modify the file path inside script.
```python
ConfigPath = "/file_path/cloudflare_dynamic_dns.config.json"
```
### Error handling 
Error message store at ```cloudflare_dynamic_dns.log```.
### Telegram alert
Using Telegram Bot, [contect BotFather](https://t.me/botfather) to create new Bot accounts.

```Telegram BOTs Token``` and ```Telegram Chat ID``` are needed. if the chat channel wasn't created, Telegram API will return ```HTTP 400 Bad Request```, You need to start the chat channel, including that bot.

## Import module
```python
# Import as module
import cloudflare_dynamic_dns

# Import the function independently
from cloudflare_dynamic_dns import UpdateSpecifyDNSRecordCANME
```

## Script
### Verify Cloudflare API Token
### Request all DNS records
### Request A record
### Request AAAA record
### Update A record
### Update AAAA record
### Update CNAME

## Dependencies
### Python version
- Python 3.7.3 or above
- Testing on the above Python version: 3.9.6 / 3.12.2
### Python module
- logging
- datetime
- json
- requests

## License
General Public License -3.0

## Resources
### My GitHub Gist
- [Verify API Token for CloudFlare API](https://gist.github.com/Suzhou65/cf63b430bfc44c03a3b1fbe2af10d6a9)
- [Get DNS record from CloudFlare API](https://gist.github.com/Suzhou65/8b9e5e5360f9c0a363e82038bb0d29b8)
- [Get IPv4, IPv6 DNS record from CloudFlare API](https://gist.github.com/Suzhou65/3488991186cbf6749b20dfc2ff5dea79)
### CloudFlare API
- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
### IP address request API
- [ipv6-test.com](https://ipv6-test.com/api/)
- [ipify](https://www.ipify.org/)