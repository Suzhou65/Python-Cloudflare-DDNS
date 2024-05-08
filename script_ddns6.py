# -*- coding: utf-8 -*-
import cloudflare_dynamic_dns
import sys

# Dynamic DNS, IPv6
def DDNSIPv6(ConfigPath):
    # Asking newest IP address
    CurrentIPv6 = cloudflare_dynamic_dns.CheckIPv6()
    # Success get current IPv4
    if type(CurrentIPv6) is str:
        # Get IP address recording in CloudFlare
        RecordIPv6 = cloudflare_dynamic_dns.RequestSpecifyDNSRecordIPv6(ConfigPath, FullyRespon=None)
        # Compare, IP address no change
        if type(CurrentIPv6) is str and CurrentIPv6 == RecordIPv6:
            return  ("DNS records and IP addresses are the same, not require update.")
        # Running update
        elif type(CurrentIPv6) is str and CurrentIPv6 != RecordIPv6:
            UpdateStatus = cloudflare_dynamic_dns.UpdateSpecifyDNSRecordIPv6(ConfigPath, UpdateDNSRecordIPv6=CurrentIPv6)
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
    elif type(CurrentIPv6) is int:
        return (f"Unable connect to IP check website, HTTP Status Code: {CurrentIPv6}.")
    # Error
    elif type(CurrentIPv6) is bool:
        return ("Error occurred during IP check, please check the error log.")

# Runtime
try:
    ConfigPath = "/file_path/cloudflare_dynamic_dns.config.json"
    CheckResult = DDNSIPv6(ConfigPath)
    print(CheckResult)
    sys.exit()
except Exception as ErrorStatus:
    print(f"Error occurred,\r\n{ErrorStatus}")
    sys.exit()

# 20240426