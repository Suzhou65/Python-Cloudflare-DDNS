# -*- coding: utf-8 -*-
from cloudflare_dynamic_dns import RequestFullyDNSRecord
import sys

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
    sys.exit()
except Exception as ErrorStatus:
    print(f"Error occurred,\r\n{ErrorStatus}")
    sys.exit()

# 20240427