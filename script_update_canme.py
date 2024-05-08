# -*- coding: utf-8 -*-
from cloudflare_dynamic_dns import UpdateSpecifyDNSRecordCANME
import sys

# Update CNAME record
def Download_DNS_Record(ConfigPath, UpdateDNSRecordCNAME):
    # Check CNAME input
    if type(UpdateDNSRecordCNAME) is dict or type(UpdateDNSRecordCNAME) is list:
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
    sys.exit()
except Exception as ErrorStatus:
    print(f"Error occurred,\r\n{ErrorStatus}")
    sys.exit()

# 20240427