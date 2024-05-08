# -*- coding: utf-8 -*-
from cloudflare_dynamic_dns import Verify
import sys

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
    sys.exit()
except Exception as ErrorStatus:
    print(f"Error occurred,\r\n{ErrorStatus}")
    sys.exit()

# 20240427