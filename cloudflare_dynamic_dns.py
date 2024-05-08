# -*- coding: utf-8 -*-
import logging
import datetime
import json
import requests

# For error handling, logfile config
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
# Error logfile name and level config
logging.basicConfig(level=logging.WARNING,filename="cloudflare_dynamic_dns.log",filemode="a",format=FORMAT)

# Generate timestamp
def GetTime():
    CurrentTime = datetime.datetime.now()
    return CurrentTime.strftime("%Y-%m-%d %H:%M:%S")

# Configuration function
def Configuration(ConfigPath, UpdateConfiguration=None):
    # Reading configuration file only
    if UpdateConfiguration is None:
        try:
            with open(ConfigPath,"r") as ConfigurationJSON:
                # Return dictionary
                ConfigurationDict = json.load(ConfigurationJSON)
                ConfigurationJSON.close()
                return ConfigurationDict
        # If configuration file not found
        except FileNotFoundError:
            logging.exception("Configuration not found, please enter basic authorization data or check file path.")
            return False
    # Update configuration file
    elif UpdateConfiguration is not None:
        try:
            # Save to JSON
            with open(ConfigPath,"w") as ConfigurationJSON:
                json.dump(UpdateConfiguration, ConfigurationJSON, indent=3)
                ConfigurationJSON.close()
                # Return dictionary if update successfully
                return UpdateConfiguration
        # If update configuration file failed
        except:
            logging.exception("Configuration file update failed.")
            return False

# Generate API request header
def RequestHeader(ConfigPath):
    # Read configuration
    ConfigurationDict = Configuration(ConfigPath)
    # Header Payload
    BearerAuth = ConfigurationDict["CloudflareAPI"]["AuthToken"]
    AuthMail = ConfigurationDict["CloudflareAPI"]["AuthMail"]
    # Using API Token as default
    return {"Authorization":BearerAuth, "X-Auth-Email":AuthMail, "Content-Type":"application/json"}

# Verify CloudFlare API, RunnableCheckPass
def Verify(ConfigPath, FullyRespon=None):
    # Verify URL
    VerifyRequest = ("https://api.cloudflare.com/client/v4/user/tokens/verify")
    # Header
    VerifyHeader = RequestHeader(ConfigPath)
    # Send verify request
    try:
        VerifyRespon = requests.get(VerifyRequest,headers=VerifyHeader,timeout=5)
        # Success, only retrun verify status
        if VerifyRespon.status_code == 200 and FullyRespon is None:
            VerifyResponDict = json.loads(VerifyRespon.text)
            VerifyRespon.close()
            return VerifyResponDict["result"]["status"]
        # Success, return full payload
        elif VerifyRespon.status_code == 200 and FullyRespon is not None:
            VerifyResponDict = json.loads(VerifyRespon.text)
            VerifyRespon.close()
            return VerifyResponDict
        # Not success
        elif VerifyRespon.status_code != 200: 
            logging.warning(VerifyRespon.status_code)
            return VerifyRespon.status_code
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Get All DNS records, RunnableCheckPass
def RequestFullyDNSRecord(ConfigPath, OutputJSONFile=None):
    # Load configuration
    ZoneDict = Configuration(ConfigPath)
    # Get Zone IDs
    ZoneID = ZoneDict["Zone"]["ZoneID"]
    # URL
    FullyDNSRecordRequest = (f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records")
    # Header
    VerifyHeader = RequestHeader(ConfigPath)
    # Send DNS record request
    try:
        FullyDNSRecordRespon = requests.get(FullyDNSRecordRequest,headers=VerifyHeader,timeout=5)
        if FullyDNSRecordRespon.status_code != 200:
            logging.warning(FullyDNSRecordRespon.status_code)
            FullyDNSRecordRespon.close()
            return FullyDNSRecordRespon.status_code
        # Success, retrun dictionary
        elif FullyDNSRecordRespon.status_code == 200 and OutputJSONFile is None:
            FullyDNSRecordResponDict = json.loads(FullyDNSRecordRespon.text)
            FullyDNSRecordRespon.close()
            return FullyDNSRecordResponDict
        # Success, save JSON file
        elif FullyDNSRecordRespon.status_code == 200 and OutputJSONFile is not None:
            FullyDNSRecordResponDict = json.loads(FullyDNSRecordRespon.text)
            FullyDNSRecordRespon.close()
            with open(OutputJSONFile,"w") as DNSRecordJSON:
                json.dump(FullyDNSRecordResponDict, DNSRecordJSON, indent=3)
                DNSRecordJSON.close()
                return [FullyDNSRecordResponDict, OutputJSONFile]
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Request specify DNS A record, RunnableCheckPass
def RequestSpecifyDNSRecordIPv4(ConfigPath, MultiRecord=None, FullyRespon=None):
    # Load configuration
    RecordDict = Configuration(ConfigPath)
    # Get Zone ID, read configuration or manually
    ZoneID = RecordDict["Zone"]["ZoneID"]
    if MultiRecord is None:
        RecordsID = RecordDict["RecordsID"]["DNSRecordIPv4ID"]
    elif MultiRecord is not None:
        RecordsID = MultiRecord
    # URL
    SpecifyDNSRecordIPv4Request = (f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records/{RecordsID}")
    # Header
    VerifyHeader = RequestHeader(ConfigPath)
    # HTTP GET
    try:
        DNSRecordIPv4Respon = requests.get(SpecifyDNSRecordIPv4Request,headers=VerifyHeader,timeout=5)
        # Success, only retrun IP address
        if DNSRecordIPv4Respon.status_code == 200 and FullyRespon is None:
            DNSRecordIPv4Dict = json.loads(DNSRecordIPv4Respon.text)
            DNSRecordIPv4Respon.close()
            DNSRecordIPv4Payload = DNSRecordIPv4Dict["result"]["content"]
            return DNSRecordIPv4Payload
        # Success, retrun fully payload
        elif DNSRecordIPv4Respon.status_code == 200 and FullyRespon is not None:
            DNSRecordIPv4Dict = json.loads(DNSRecordIPv4Respon.text)
            DNSRecordIPv4Respon.close()
            return DNSRecordIPv4Dict
        elif DNSRecordIPv4Respon.status_code != 200:
            logging.warning(DNSRecordIPv4Respon.status_code)
            DNSRecordIPv4Respon.close()
            return DNSRecordIPv4Respon.status_code
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Update specify DNS A records, RunnableCheckPass
def UpdateSpecifyDNSRecordIPv4(ConfigPath, MultiRecord=None, UpdateDNSRecordIPv4=()):
    # Load configuration
    RecordDict = Configuration(ConfigPath)
    # Value mapping, read configuration or manually
    ZoneID = RecordDict["Zone"]["ZoneID"]
    if MultiRecord is None:
        RecordsID = RecordDict["RecordsID"]["DNSRecordIPv4ID"]
        DomainName = RecordDict["RecordsID"]["DNSRecordIPv4Domain"]
        ProxyAbility = RecordDict["RecordsID"]["DNSRecordIPv4ProxyAble"]
        ProxyMode = RecordDict["RecordsID"]["DNSRecordIPv4ProxyMode"]
    elif MultiRecord is not None:
        RecordsID = MultiRecord[0]
        DomainName = MultiRecord[1]
        ProxyAbility = MultiRecord[2]
        ProxyMode = MultiRecord[3]
    # Payload
    UpdateSpecifyDNSRecordIPv4Dict = {
        "type":"A",
        "name":DomainName,
        "content":UpdateDNSRecordIPv4,
        "proxiable":ProxyAbility,
        "proxied":ProxyMode,
        "ttl":1}
    # Turn into JSON payload
    UpdateSpecifyDNSRecordIPv4JSON = json.dumps(UpdateSpecifyDNSRecordIPv4Dict)
    # URL
    SpecifyDNSRecordIPv4update = (f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records/{RecordsID}")
    # Header
    VerifyHeader = RequestHeader(ConfigPath)
    # HTTP PUT
    try:
        SpecifyDNSRecordIPv4Result = requests.put(SpecifyDNSRecordIPv4update,headers=VerifyHeader,data=UpdateSpecifyDNSRecordIPv4JSON,timeout=5)
        # Update DNS record successfully
        if SpecifyDNSRecordIPv4Result.status_code == 200:
            SpecifyDNSRecordIPv4ResultDict = json.loads(SpecifyDNSRecordIPv4Result.text)
            SpecifyDNSRecordIPv4Result.close()
            # Update configuration
            UpdateConfiguration = RecordDict
            # Mark Update time
            DNSRecordIPv4UpdateTime = GetTime()
            UpdateConfiguration["IPAddressUpdateRecord"]["DNSRecordIPv4UpdateTime"] = DNSRecordIPv4UpdateTime
            # Logging IPv4 address if updating single record
            if MultiRecord is None:
                UpdateConfiguration["IPAddressUpdateRecord"]["DNSRecordIPv4"] = UpdateDNSRecordIPv4
            # Ignore logging in manual mode
            elif MultiRecord is not None:
                pass
            # Update configuration file
            Configuration(ConfigPath, UpdateConfiguration)
            # Return dictionary
            return SpecifyDNSRecordIPv4ResultDict
        elif SpecifyDNSRecordIPv4Result.status_code != 200:
            logging.warning(SpecifyDNSRecordIPv4Result.status_code)
            SpecifyDNSRecordIPv4Result.close()
            return SpecifyDNSRecordIPv4Result.status_code
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Request specify DNS AAAA record, RunnableCheckPass
def RequestSpecifyDNSRecordIPv6(ConfigPath, MultiRecord=None, FullyRespon=None):
    # Load configuration
    RecordDict = Configuration(ConfigPath)
    # Get Zone ID, read configuration or manually
    ZoneID = RecordDict["Zone"]["ZoneID"]
    if MultiRecord is None:
        RecordsID = RecordDict["RecordsID"]["DNSRecordIPv6ID"]
    elif MultiRecord is not None:
        RecordsID = MultiRecord    
    # URL
    SpecifyDNSRecordIPv6Request = (f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records/{RecordsID}")
    # Header
    VerifyHeader = RequestHeader(ConfigPath)
    # HTTP GET
    try:
        DNSRecordIPv6Respon = requests.get(SpecifyDNSRecordIPv6Request,headers=VerifyHeader,timeout=5)
        # Success, only retrun IP address
        if DNSRecordIPv6Respon.status_code == 200 and FullyRespon is None:
            DNSRecordIPv6Dict = json.loads(DNSRecordIPv6Respon.text)
            DNSRecordIPv6Respon.close()
            DNSRecordIPv6Payload = DNSRecordIPv6Dict["result"]["content"]
            return DNSRecordIPv6Payload
        # Success, retrun fully payload
        elif DNSRecordIPv6Respon.status_code == 200 and FullyRespon is not None:
            DNSRecordIPv6Dict = json.loads(DNSRecordIPv6Respon.text)
            DNSRecordIPv6Respon.close()
            return DNSRecordIPv6Dict
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Update specify DNS AAAA records, RunnableCheckPass
def UpdateSpecifyDNSRecordIPv6(ConfigPath, MultiRecord=None, UpdateDNSRecordIPv6=()):
    # Load configuration
    RecordDict = Configuration(ConfigPath)
    # Value mapping, read configuration or manually
    ZoneID = RecordDict["Zone"]["ZoneID"]
    if MultiRecord is None:
        RecordsID = RecordDict["RecordsID"]["DNSRecordIPv6ID"]
        DomainName = RecordDict["RecordsID"]["DNSRecordIPv6Domain"]
        ProxyAbility = RecordDict["RecordsID"]["DNSRecordIPv6ProxyAble"]
        ProxyMode = RecordDict["RecordsID"]["DNSRecordIPv6ProxyMode"]
    elif MultiRecord is not None:
        RecordsID = MultiRecord[0]
        DomainName = MultiRecord[1]
        ProxyAbility = MultiRecord[2]
        ProxyMode = MultiRecord[3]
    # Payload
    UpdateSpecifyDNSRecordIPv6Dict = {
        "type":"AAAA",
        "name":DomainName,
        "content":UpdateDNSRecordIPv6,
        "proxiable":ProxyAbility,
        "proxied":ProxyMode,
        "ttl":1}
    # Turn into JSON payload
    UpdateSpecifyDNSRecordIPv6JSON = json.dumps(UpdateSpecifyDNSRecordIPv6Dict)
    # URL
    SpecifyDNSRecordIPv6update = (f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records/{RecordsID}")
    # Header
    VerifyHeader = RequestHeader(ConfigPath)
    # HTTP PUT
    try:
        SpecifyDNSRecordIPv6Result = requests.put(SpecifyDNSRecordIPv6update,headers=VerifyHeader,data=UpdateSpecifyDNSRecordIPv6JSON,timeout=5)
        # Update DNS record successfully
        if SpecifyDNSRecordIPv6Result.status_code == 200:
            SpecifyDNSRecordIPv4ResultDict = json.loads(SpecifyDNSRecordIPv6Result.text)
            SpecifyDNSRecordIPv6Result.close()
            # Update configuration
            UpdateConfiguration = RecordDict
            # Mark Update time
            DNSRecordIPv6UpdateTime = GetTime()
            UpdateConfiguration["IPAddressUpdateRecord"]["DNSRecordIPv6UpdateTime"] = DNSRecordIPv6UpdateTime
            # Logging IPv6 address if updating single record
            if MultiRecord is None:
                UpdateConfiguration["IPAddressUpdateRecord"]["DNSRecordIPv6"] = UpdateDNSRecordIPv6
            # Ignore logging in manual mode
            elif MultiRecord is not None:
                pass
            # Update configuration file
            Configuration(ConfigPath, UpdateConfiguration)
            # Return dictionary
            return SpecifyDNSRecordIPv4ResultDict
        elif SpecifyDNSRecordIPv6Result.status_code != 200:
            logging.warning(SpecifyDNSRecordIPv6Result.status_code)
            SpecifyDNSRecordIPv6Result.close()
            return SpecifyDNSRecordIPv6Result.status_code
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Update DNS CNAME records, RunnableCheckPass
def UpdateSpecifyDNSRecordCANME(ConfigPath, UpdateDNSRecordCNAME):
    # Load configuration
    RecordDict = Configuration(ConfigPath)
    # Mode select, import from configuration
    if len(UpdateDNSRecordCNAME) == 2:
        ZoneID = RecordDict["Zone"]["ZoneID"]
        RecordsID = RecordDict["CNAME"]["DNSRecordCNAMEID"]
        RecordNAME = UpdateDNSRecordCNAME[0]
        RecordTarget = UpdateDNSRecordCNAME[1]
        # URL
        CNAMEupdate = (f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records/{RecordsID}")
        # Payload
        UpdateSpecifyDNSRecordCNAMEDict = {
            "type":"CNAME",
            "name":RecordNAME,
            "content":RecordTarget,
            "proxiable":False,
            "proxied":False,
            "ttl":1}
    # Mode select, import CNAME configuration by script
    elif len(UpdateDNSRecordCNAME) == 3:
        ZoneID = RecordDict["Zone"]["ZoneID"]
        RecordsID = UpdateDNSRecordCNAME[0]
        RecordNAME = UpdateDNSRecordCNAME[1]
        RecordTarget = UpdateDNSRecordCNAME[2]
        # URL
        CNAMEupdate = (f"https://api.cloudflare.com/client/v4/zones/{ZoneID}/dns_records/{RecordsID}")
        # Payload
        UpdateSpecifyDNSRecordCNAMEDict = {
            "type":"CNAME",
            "name":RecordNAME,
            "content":RecordTarget,
            "proxiable":False,
            "proxied":False,
            "ttl": 1}
    # Turn into JSON payload
    UpdateCNAMEJSON = json.dumps(UpdateSpecifyDNSRecordCNAMEDict)
    # Header
    VerifyHeader = RequestHeader(ConfigPath)
    # HTTP PUT
    try:
        CNAMEupdateRequest = requests.put(CNAMEupdate,headers=VerifyHeader,data=UpdateCNAMEJSON,timeout=5)
        # Success, update configuration file
        if CNAMEupdateRequest.status_code == 200 and len(UpdateDNSRecordCNAME) == 2:
            CNAMEupdateRespon = json.loads(CNAMEupdateRequest.text)
            CNAMEupdateRequest.close()
            # Update configuration
            UpdateConfigurationdDict = RecordDict
            # Mark Update time
            DNSRecordCNAMEUpdateTime = GetTime()
            UpdateConfigurationdDict["CNAME"]["DNSRecordCNAMEUpdateTime"] = DNSRecordCNAMEUpdateTime
            # Logging CNAME
            UpdateConfigurationdDict["CNAME"]["NAME"] = RecordNAME
            UpdateConfigurationdDict["CNAME"]["TARGET"] = RecordTarget
            # Update configuration file
            Configuration(ConfigPath, UpdateConfiguration=UpdateConfigurationdDict)
            # Return dictionary
            return CNAMEupdateRespon
        # Success, retrun payload only
        elif CNAMEupdateRequest.status_code == 200 and len(UpdateDNSRecordCNAME) == 3:
            CNAMEupdateRespon = json.loads(CNAMEupdateRequest.text)
            CNAMEupdateRequest.close()
            return CNAMEupdateRespon
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Get IPv4, RunnableCheckPass
def CheckIPv4():
    # Check from ipify
    try:
        # Header
        ParamsIPify = {"format":"json"}
        ParamsIPtest = ("json")
        # Request IPify4
        RequestIPify4 = requests.get("https://api.ipify.org/",params=ParamsIPify,timeout=5)
        if RequestIPify4.status_code == 200:
            IPify4JSON = json.loads(RequestIPify4.text)
            RequestIPify4.close()
            # Get string from dictionary
            return IPify4JSON["ip"]
        elif RequestIPify4.status_code != 200:
            # Retry, check from IPtest
            RequestIPtest4 = requests.get("https://v4.ipv6-test.com/api/myip.php",params=ParamsIPtest,timeout=10)
            if RequestIPtest4.status_code == 200:
                IPtest4JSON = json.loads(RequestIPtest4.text)
                RequestIPtest4.close()
                return IPtest4JSON["address"]
            elif RequestIPtest4.status_code != 200:
                return RequestIPtest4.status_code
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Get IPv6, RunnableCheckPass
def CheckIPv6():
    # Check from ipify
    try:
        # Header
        ParamsIPify = {"format":"json"}
        ParamsIPtest = ("json")
        # Request IPify4
        RequestIPify6 = requests.get("https://api64.ipify.org/",params=ParamsIPify,timeout=5)
        if RequestIPify6.status_code == 200:
            IPify6JSON = json.loads(RequestIPify6.text)
            RequestIPify6.close()
            # Get string from dictionary
            return IPify6JSON["ip"]
        elif RequestIPify6.status_code != 200:
            # Retry, check from IPtest
            RequestIPtest6 = requests.get("https://v6.ipv6-test.com/api/myip.php",params=ParamsIPtest,timeout=10)
            if RequestIPtest6.status_code == 200:
                IPtest6JSON = json.loads(RequestIPtest6.text)
                RequestIPtest6.close()
                return IPtest6JSON["address"]
            elif RequestIPtest6.status_code != 200:
                return RequestIPtest6.status_code
    # Error
    except Exception as ErrorStatus:
        logging.exception(ErrorStatus)
        return False

# Sending telegram message via bots, WARNING Not tested
def SendAlert(ConfigPath, MessagePayload):
    # Load configuration
    MessageConfig = Configuration(ConfigPath)
    TelegramBotToken = MessageConfig["Telegram_BOTs"]["TelegramToken"]
    TelegramReceiver = MessageConfig["Telegram_BOTs"]["TelegramChatID"]
    # Check telegram BOTs configuration
    if len(TelegramBotToken) == 0 or len(TelegramReceiver) == 0:
        return ("Telegram configuration not found, please initialize.")
    # Find configuration
    else:
        # Make telegram url
        TelegramBotURL = (f"https://api.telegram.org/bot{TelegramBotToken}/sendMessage")
        TelegramJsonPayload = {"chat_id":TelegramReceiver,"text":MessagePayload}
        # Sending telegram 
        try:
            TelegramResponse = requests.post(TelegramBotURL,json=TelegramJsonPayload)
            if TelegramResponse.status_code == 200:
                TelegramResponse.close()
                return 200
            # Chat channel wasn't create
            elif TelegramResponse.status_code == 400:
                TelegramResponse.close()
                return ("Chat channel wasn't create.")
            # Other error
            elif TelegramResponse.status_code != 200 or 400:
                TelegramResponse.close()
                return (f"Telegram API respons: {TelegramResponse.status_code}.")
        except Exception as ErrorStatus:
            logging.exception(ErrorStatus)
            return False

# 20240505