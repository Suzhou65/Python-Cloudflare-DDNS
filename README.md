# Python-Cloudflare-DDNS
[![Python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![AM](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/CloudFlare-Dynamic-DNS)
[![Size](https://img.shields.io/github/repo-size/Suzhou65/Python-Cloudflare-DDNS.svg)](https://shields.io/category/size)

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
Please reference to the demo script ```script_verify.py```.
```python
from cloudflare_dynamic_dns import Verify
# Check authorize status
def VerifyCheck(ConfigPath, FullyRespon):
    CheckResult = Verify(ConfigPath,FullyRespon)
    # Error
    if type(CheckResult) is bool:
        return ("Error occurred during connect to Cloudflare API, please check the error log.")
    # Get HTTP status code
    elif type(CheckResult) is int:
        return (f"Unable connect to Cloudflare API, HTTP Status Code: {CheckResult}.")
    # Output fully Cloudflare API Respon
    elif type(CheckResult) is dict:
        return (f"Cloudflare API Response:\r\n.{CheckResult}")
    # Print authorize status only
    elif type(CheckResult) is str:
        return (f"The token authorize status is: {CheckResult}.")
# Runtime
try:
    ConfigPath = "/file_path/cloudflare_dynamic_dns.config.json"
    # If enable FullyRespon, script will print out fully Cloudflare API respon as dictionary
    FullyRespon = None
    CheckResult = VerifyCheck(ConfigPath,FullyRespon)
    print(CheckResult)
```
### Request all DNS records
Please reference to the demo script ```script_request_fully.py```. Default will output as Python Dictionary, define ```OutputJSONFile``` to output JSON file. 
```python
from cloudflare_dynamic_dns import RequestFullyDNSRecord
# Download DNS record
def Download_DNS_Record(ConfigPath, OutputJSONFile):
    ResultDict = RequestFullyDNSRecord(ConfigPath, OutputJSONFile)
    # Error
    if type(ResultDict) is bool:
        return ("Error occurred during connect to Cloudflare API, please check the error log.")
    # Get HTTP status code
    elif type(ResultDict) is int:
        return (f"Unable connect to Cloudflare API, HTTP Status Code: {ResultDict}.")
    # Output fully Cloudflare API Respon
    elif type(ResultDict) is dict:
        return (f"Cloudflare API Response:\r\n.{ResultDict}")
    # Print authorize status only
    elif type(ResultDict) is list:
        JSONFilePath = ResultDict[1]
        return (f"Cloudflare API Response Storage at: {JSONFilePath}")
# Runtime
try:
    # Configuration file path
    ConfigPath = "/file_path/cloudflare_dynamic_dns.config.json"
    # Output all DNS record as JSON file or not, Disable will print out as dictionary
    OutputJSONFile = None
    AskRecordResult = Download_DNS_Record(ConfigPath,OutputJSONFile)
    print(AskRecordResult)
except Exception as ErrorStatus:
    print(f"Error occurred,\r\n{ErrorStatus}")
```
### Request A record
```python
import cloudflare_dynamic_dns
# Configuration file path
ConfigPath = "/file_path/cloudflare_dynamic_dns.config.json"
# Asking Cloudflare API
RecordIPv4 = cloudflare_dynamic_dns.RequestSpecifyDNSRecordIPv4(ConfigPath, FullyRespon=None)
# Print result
print(RecordIPv4)
```
Basic respon specify ```RecordsID``` reference to configuration. If you wish to request multiple or specify DNS A record manually, please define ```MultiRecord```.
### Request AAAA record
```python
import cloudflare_dynamic_dns
# Configuration file path
ConfigPath = "/file_path/cloudflare_dynamic_dns.config.json"
# Asking Cloudflare API
RecordIPv6 = cloudflare_dynamic_dns.RequestSpecifyDNSRecordIPv6(ConfigPath, FullyRespon=None)
# Print result
print(RecordIPv6)
```
Basic respon specify ```RecordsID``` reference to configuration. If you wish to request multiple or specify DNS AAAA record manually, please define ```MultiRecord```.
### Update A record
Please reference to the DDNS demo script ```script_ddns4.py```.
```python
import cloudflare_dynamic_dns
# Update DNS A record
UpdateStatus = cloudflare_dynamic_dns.UpdateSpecifyDNSRecordIPv4(ConfigPath, UpdateDNSRecordIPv4=CurrentIPv4)
# Get Cloudflare API respon
if type(UpdateStatus) is dict:
  # Return success or not
  SuccessOrNot = UpdateStatus["success"]
  print(f"Cloudflare API Responses: {SuccessOrNot}.")
# Get HTTP status code
elif type(UpdateStatus) is int:
  print(f"Unable connect to Cloudflare API, HTTP Status Code: {UpdateStatus}.")
# Error
elif type(UpdateStatus) is bool:
  print("Error occurred during connect to Cloudflare API, please check the error log.")
```
Basis update using Python String, please define IP address ```UpdateDNSRecordIPv4```. If you wish to update multiple or specify DNS AAAA record, please define ```MultiRecord``` which including ```RecordsID```, ```Domain Name```, ```Proxy Ability``` and ```Proxy Mode```, packing as Python List.
```python
# Array
UpdateArray = ["RecordsID", "Domain Name", True, True]
# Update record
cloudflare_dynamic_dns.UpdateSpecifyDNSRecordIPv4(ConfigPath, MultiRecord=UpdateArray, UpdateDNSRecordIPv4=CurrentIPv4)
```
### Update AAAA record
Please reference to the DDNS demo script ```script_ddns6.py```.
```python
import cloudflare_dynamic_dns
UpdateStatus = cloudflare_dynamic_dns.UpdateSpecifyDNSRecordIPv6(ConfigPath, UpdateDNSRecordIPv6=CurrentIPv6)
# Get Cloudflare API respon
if type(UpdateStatus) is dict:
  # Return success or not
  SuccessOrNot = UpdateStatus["success"]
  print(f"Cloudflare API Responses: {SuccessOrNot}.")
# Get HTTP status code
elif type(UpdateStatus) is int:
  print(f"Unable connect to Cloudflare API, HTTP Status Code: {UpdateStatus}.")
# Error
elif type(UpdateStatus) is bool:
  print("Error occurred during connect to Cloudflare API, please check the error log.")
```
Basis update using Python String, please define IP address ```UpdateDNSRecordIPv6```. If you wish to update multiple or specify DNS AAAA record, please define ```MultiRecord``` which including ```RecordsID```, ```Domain Name```, ```Proxy Ability``` and ```Proxy Mode```, packing as Python List.
```python
# Array
UpdateArray = ["RecordsID", "Domain Name", True, True]
# Update record
cloudflare_dynamic_dns.UpdateSpecifyDNSRecordIPv6(ConfigPath, MultiRecord=UpdateArray, UpdateDNSRecordIPv4=CurrentIPv6)
```
### Update CNAME
Please reference to the DDNS demo script ```script_update_canme.py```.
```python
from cloudflare_dynamic_dns import UpdateSpecifyDNSRecordCANME
# Update CNAME record
def Download_DNS_Record(ConfigPath, UpdateDNSRecordCNAME):
    # Check CNAME input
    if type(UpdateDNSRecordCNAME) is list:
        ResultDict = UpdateSpecifyDNSRecordCANME(ConfigPath, UpdateDNSRecordCNAME)
        # Error
        if type(ResultDict) is bool:
            return ("Error occurred during connect to Cloudflare API, please check the error log.")
        # Get HTTP status code
        elif type(ResultDict) is int:
            return (f"Unable connect to Cloudflare API, HTTP Status Code: {ResultDict}.")
        # Output fully Cloudflare API Respon
        elif type(ResultDict) is dict:
            return ResultDict
    # Print authorize status only
    else:
        return (f"Unable running CNAME update. Please check input configuration.")
# Runtime
try:
    # Configuration file path
    ConfigPath = "/file_path/cloudflare_dynamic_dns.config.json"
    # CNAME update with list input
    UpdateDNSRecordCNAME = ["name.cloudflare.dns","target.cloudflare.dns"]
    CNAMEUpdateResult = Download_DNS_Record(ConfigPath, UpdateDNSRecordCNAME)
    if type(CNAMEUpdateResult) is dict:
        SuccessOrNot = CNAMEUpdateResult["success"]
        print(f"Cloudflare API Responses: {SuccessOrNot}.")
    else:
        print(CNAMEUpdateResult)
except Exception as ErrorStatus:
    print(f"Error occurred,\r\n{ErrorStatus}")
```
Basis update using Python List, please define CNAME ```NAME``` and ```VALUE``` inside ```UpdateDNSRecordCNAME```. If you wish to update multiple or specify CNAME record, please define ```UpdateDNSRecordCNAME``` including ```RecordsID```.
```python
# Specify CNAME
UpdateDNSRecordCNAME = ["Cloudflare_DNS_Records_ID", "name.cloudflare.dns", "target.cloudflare.dns"]
```

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