#! /usr/bin/env python3
#############################################
#                                           #
#       Dynamic Inventory Generator         #
#                   by                      #
#            Injected Fusion                #
#                                           #
# Version 0.1.1 - Tested with: Python 3.8.2 #
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
from iteration_utilities import unique_everseen


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

def file_contents(path_to_file):
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
        return (output)


def site_names_map(path_to_map_file):
    with open('./mappings/sites.json') as f:
        sites = json.load(f)
    return sites


contents = file_contents('./tmp/hosts')
#pp.pprint (content)

site_names = site_names_map('./mappings/sites.json')
pp.pprint (site_names)

def replace_site_names(contents, site_names):
#    site_expanded = []

    for c in contents:
#        print(c['site_name'])
        expanded_site_name = site_names[c['site_name']]
#        print(expanded_site_name)
        # replace site name abbreviation with expanded site name
        c['site_name'] = expanded_site_name
        print(c)

    # iterate over content
thing = replace_site_names(contents, site_names)
#pp.pprint (thing)

# Transform site names from mappings
#groups = [li['site_name'] for li in content]

#def replace(list, dictionary):
#    dict = {'groups':[sites.get(item, item) for item in list] }
#    return [sites.get(item, item) for item in list]


# Remove duplicates from groupings
#children = (list(unique_everseen(replace(groups,sites))))

#dict2 = {'groups':
#    children
#}

#pp.pprint (dict2)