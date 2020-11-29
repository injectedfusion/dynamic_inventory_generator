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
import pprint
pp = pprint.PrettyPrinter(indent=1)
from operator import itemgetter
from iteration_utilities import unique_everseen


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

def file_contents(path_to_file):
    output = []
    with open(path_to_file) as a_file:
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


def site_names_map(path_to_file):
    with open(path_to_file) as f:
        sites = json.load(f)
    return sites

def device_types_map(path_to_file):
    with open(path_to_file) as f:
        device_types = json.load(f)
    return device_types

# Takes a string formatted like this: 'Disneyland Resort Anaheim'
# and converts it to be formatted like this: 'disneyland_resort_anaheim'
def sanitized_name(name):
    lower_case_name = name.lower()
    sanitized_name = lower_case_name.replace(" ", "_")
    return sanitized_name

def replace_site_names(contents, site_names):
    
    for c in contents:
        expanded_site_name = site_names[c['site_name']]

        # replace site name abbreviation with expanded 
        # and sanitized site name
        c['site_name'] = sanitized_name(expanded_site_name)

    return contents

def replace_device_types(contents, device_types):
    for c in contents:
        expanded_device_type = device_types[c['device_type']]

        # replace site name abbreviation with expanded 
        # and sanitized site name
        c['device_type'] = sanitized_name(expanded_device_type)

    return contents

# Create a dictionary of dictionaries
# where each dictionary corresponds to a 
# site name (and one big dictionary holds
# all of them)
def site_dictionary(site_names):
    site_dictionary = {}

    for s in site_names:
        site_name = site_names[s]
        site_key = sanitized_name(site_name)
        site_dictionary[site_key] = []
    
    return site_dictionary

# Sort the entries by Site name
def sort_by_site_name(expanded_site_names_contents, site_names):
    container_dictionary = site_dictionary(site_names)

    for entry in expanded_site_names_content:
        site_name = entry['site_name']

        container_dictionary[site_name].append(entry)

    return container_dictionary

# Takes an individual site_name dictionary
# Then sorts it by unit_name
def sort_by_unit_name(site_name_dictionary):
    unit_sorted_dictionary = {}

    for entry in site_name_dictionary:
        unit_name = sanitized_name(entry['unit_name'])

        # Check if the unit name has already
        # been added as a key in the unit dictionary
        if unit_name in unit_sorted_dictionary:
            # if it is, do not create it again
            # just append it to the existing one
            unit_sorted_dictionary[unit_name].append(entry)
        else:
            # if it is not, create the key
            unit_sorted_dictionary[unit_name] = [entry]

    return unit_sorted_dictionary

def sort_by_device_type(device_dictionary):
    device_type_sorted_dictionary = {}

    for device in device_dictionary:
#        pp.pprint(device)
       device_type = sanitized_name(device['device_type'])
#       pp.pprint(device_type)
        # Check if the device type has already
        # been added as a key in the devices dictionary
       if device_type in device_type_sorted_dictionary:
           device_type_sorted_dictionary[device_type].append(device)
       else: 
           device_type_sorted_dictionary[device_type] = [device]

    return device_type_sorted_dictionary

def formatted_data(expanded_site_names_content, site_names):
    # First, sort by site name
    sorted_site_name_data = sort_by_site_name(expanded_site_names_content, site_names)
   # pp.pprint(sorted_site_name_data)

    # Now, sort each site by unit name
    for site in site_names:
        site_entry_name = sanitized_name(site_names[site])
        site_entry = sorted_site_name_data[site_entry_name]

        # First, let's sort by unit
        unit_sorted_dictionary = sort_by_unit_name(site_entry)

        # Now sort each unit by device type
        for unit, devices in unit_sorted_dictionary.items():
            device_sorted_inventory = sort_by_device_type(devices)
            # pp.pprint(unit_sorted_dictionary[unit])
            unit_sorted_dictionary[unit].clear()
            unit_sorted_dictionary[unit] = device_sorted_inventory
        
        # Clear the entry for the site name in the dictionary
        sorted_site_name_data[site_entry_name].clear()

        # Then set the entry to be the unit_sorted_dictionary
        sorted_site_name_data[site_entry_name] = unit_sorted_dictionary


    return sorted_site_name_data

contents = file_contents('./tmp/hosts')
site_names = site_names_map('./mappings/sites.json')
device_types = device_types_map('./mappings/devices.json')
#pp.pprint(device_types)

expanded_site_names_content = replace_site_names(contents, site_names)
expanded_device_types_content = replace_device_types(contents, device_types)

#pp.pprint(expanded_device_types_content)
formatted_dictionary = formatted_data(expanded_site_names_content, site_names)

pp.pprint(formatted_dictionary)