# -*- coding: utf-8 -*-
import cloudflare_dynamic_dns
import sys

# Dynamic DNS, IPv4
def DDNSIPv4(ConfigPath):
    # Asking newest IP address
    CurrentIPv4 = cloudflare_dynamic_dns.CheckIPv4()
    # Success get current IPv4
    if type(CurrentIPv4) is str:
        # Get IP address recording in CloudFlare
        RecordIPv4 = cloudflare_dynamic_dns.RequestSpecifyDNSRecordIPv4(ConfigPath, FullyRespon=None)
        # Compare, IP address no change
        if type(RecordIPv4) is str and CurrentIPv4 == RecordIPv4:
            return  ("DNS records and IP addresses are the same, not require update.")
        # Running update
        elif type(RecordIPv4) is str and CurrentIPv4 != RecordIPv4:
            UpdateStatus = cloudflare_dynamic_dns.UpdateSpecifyDNSRecordIPv4(ConfigPath, UpdateDNSRecordIPv4=CurrentIPv4)
            # Get Cloudflare API respon
            if type(UpdateStatus) is dict:
                # Return success or not
                SuccessOrNot = UpdateStatus["success"]
                return (f"Cloudflare API Responses: {SuccessOrNot}.")
            # Get HTTP status code
            elif type(UpdateStatus) is int:
                return (f"Unable connect to Cloudflare API, HTTP Status Code: {UpdateStatus}.")
            # Error
            elif type(UpdateStatus) is bool:
                return ("Error occurred during connect to Cloudflare API, please check the error log.")
    # Get HTTP status code
    elif type(CurrentIPv4) is int:
        return (f"Unable connect to IP check website, HTTP Status Code: {CurrentIPv4}.")
    # Error
    elif type(CurrentIPv4) is bool:
        return ("Error occurred during IP check, please check the error log.")

# Runtime
try:
    ConfigPath = "/file_path/cloudflare_dynamic_dns.config.json"
    CheckResult = DDNSIPv4(ConfigPath)
    print(CheckResult)
    sys.exit()
except Exception as ErrorStatus:
    print(f"Error occurred,\r\n{ErrorStatus}")
    sys.exit()

# 20240424