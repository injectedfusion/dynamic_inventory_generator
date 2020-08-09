#! /usr/bin/env python3
#############################################
#                                           #
#       Dynamic Inventory Generator         #
#                   by                      #
#            Injected Fusion                #
#                                           #
#  Version 0.1 - Tested with: Python 3.8.2  #
#                                           #
#############################################

import json
import re
import collections


# Open Sites Mapping
with open('./mappings/sites.json') as f:
    sites = json.load(f)

# Pre-compile regular expresions into an object
# Courtesy of https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
ValidIpAddressRegex = re.compile(r'''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                          25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                          25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                          25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)''')

SiteCodeRegex = re.compile(r'''(?<=\b)[a-zA-Z0-9]{4}(?=-)''')
DevicesRegex = re.compile(r'''(?<=-)[a-z]{2}(?<!-)''')
UnitNameRegex = re.compile(r'''(?<=:\s\s).*$''')


sample = '''172.18.0.128             DR13-u00-os-01a         ## OWNER:  Rescue Rangers'''

ipv4_result     = ValidIpAddressRegex.search(sample)
device_result   = DevicesRegex.search(sample)
site_result     = SiteCodeRegex.search(sample)
unit_result     = UnitNameRegex.search(sample)

dict={'ipv4_address':ipv4_result.group(0),'device':device_result.group(0)}
print(dict)



# def reader():
#     values = {}
#     with open('./tmp/hosts') as a_file:
#         Lines = a_file.readlines()
#         for line in Lines:
#             values = dict{'ipv4_address':ValidIpAddressRegex.match(line)}
#             print(values)
           