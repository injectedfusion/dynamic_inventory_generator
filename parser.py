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

import os
import sys
import argparse
import json
import re
import collections
# import pyyaml
import pprint
pp = pprint.PrettyPrinter(indent=1)
from operator import itemgetter


# Open Sites Mapping
with open('./mappings/sites.json') as f:
    sites = json.load(f)


# Pre-compile regular expresions into an object
# Courtesy of https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
ValidIpAddressRegex = re.compile(r'''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                          25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                          25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                          25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)''')

SiteCodeRegex       = re.compile(r'''(?<=\b)[a-zA-Z0-9]{4}(?=-)''')
DevicesRegex        = re.compile(r'''(?<=-)[a-z]{2}(?<!-)''')
UnitNameRegex       = re.compile(r'''(?<=:\s\s).*$''')
HostNameRegex       = re.compile(r'''(?<=\b)[a-zA-Z0-9]{4}-[a-zA-Z0-9]{3}-[a-zA-Z0-9]{2}-[a-zA-Z0-9]{3}(?=\b)''')



# class DynamicInventory(object):

#     def __init__(self):
#         self.inventory = {}
#         self.read_cli_args()

#         # Called with `--list`
#         if self.args.list:
#             self.inventory = self.dynamic_inventory()
#         # Called with `--host [hostname]`.
#         elif self.args.host:
#             # Not implemented, sinced we return _meta info `--list`
#             self.inventory = self.dynamic_inventory()

def reader():
    output = []
    with open('./tmp/hosts') as a_file:
        Lines = a_file.readlines()
        for line in Lines:
            ipv4_result     = ValidIpAddressRegex.search(line)
            device_result   = DevicesRegex.search(line)
            site_result     = SiteCodeRegex.search(line)
            unit_result     = UnitNameRegex.search(line)
            host_result     = HostNameRegex.search(line)
            dict = {'ipv4_address':ipv4_result.group(0),'host_name':host_result.group(0),'device_type':device_result.group(0),'site_name':site_result.group(0),'unit_name':unit_result.group(0)}
            output += [dict]
        # pp.pprint(output)
        return (output)


groups = [li['site_name'] for li in reader()]

def replace(list, dictionary):
    dict = {'groups':[sites.get(item, item) for item in list] }
    return [sites.get(item, item) for item in list]


# pp.pprint(replace(groups,sites))

dict2 = {'groups':
    (replace(groups,sites))
}

pp.pprint (dict2)