#! /usr/bin/env python3
#############################################
#                                           #
#       Dynamic Inventory Generator         #
#                   by                      #
#     injectedfusion & nellshamrell         #
#                                           #
# Version 0.2.0                             #
# Tested with: Python 3.8.2                 #
# Tested with: Python 3.8.5                 #
# Tested with: Python 3.9                   #
#                                           #
#############################################

import json
import re
import yaml
import pprint

pp = pprint.PrettyPrinter(indent=1)

# Pre-compile regular expressions into an object
# Courtesy of https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
ValidIpAddressRegex = re.compile(r'''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)''')
SiteCodeRegex = re.compile(r'''(?<=\b)[a-zA-Z0-9]{4}(?=-)''')
DevicesRegex = re.compile(r'''(?<=-)[a-z]{2}(?<!-)''')
UnitNameRegex = re.compile(r'''(?<=:\s\s).*$''')
HostNameRegex = re.compile(r'''(?<=\b)[a-zA-Z0-9]{4}-[a-zA-Z0-9]{3}-[a-zA-Z0-9]{2}-[a-zA-Z0-9]{3}(?=\b)''')


def file_contents(path_to_file):
    file_output = []
    with open(path_to_file) as a_file:
        lines = a_file.readlines()
        for line in lines:
            ipv4_result = ValidIpAddressRegex.search(line)
            device_result = DevicesRegex.search(line)
            site_result = SiteCodeRegex.search(line)
            unit_result = UnitNameRegex.search(line)
            host_result = HostNameRegex.search(line)
            base_dict = {'ipv4_address': ipv4_result.group(0), 'host_name': host_result.group(0),
                         'device_type': device_result.group(0), 'site_name': site_result.group(0),
                         'unit_name': unit_result.group(0)}
            file_output += [base_dict]
        return file_output


def site_names_map(path_to_file):
    with open(path_to_file) as f:
        sites = json.load(f)
    return sites


def device_types_map(path_to_file):
    with open(path_to_file) as f:
        device_types = json.load(f)
    return device_types


# Takes an abbreviated name and a map file for the abbreviations.
# Then returns the full name associated with the abbreviation.


def expanded_name(name, new_map):
    expanded_name = new_map[name]
    return expanded_name


# Takes a string formatted like this: 'Disneyland Resort Anaheim'
# and converts it to be formatted like this: 'disneyland_resort_anaheim'


def sanitized_name(name):
    lower_case_name = name.lower()
    sanitized_name = lower_case_name.replace(" ", "_")
    return sanitized_name


def setup_inventory_dictionary():
    inventory_dictionary = {
        'all': {
            'hosts': {},
            'children': {}
        }
    }

    return inventory_dictionary


def formatted_hosts_json(input_contents, site_names_map, device_types_map):
    inventory_dictionary = setup_inventory_dictionary()

    for entry in input_contents:
        expanded_site_name = expanded_name(entry['site_name'], site_names_map)
        site_name = sanitized_name(expanded_site_name)

        # Check if the site name already exists
        # as a key in the inventory_dictionary dictionary
        # if it does not already exist, add it
        # and set it to an empty dictionary
        if site_name not in inventory_dictionary['all']['children']:
            inventory_dictionary['all']['children'][site_name] = {}

        # Now, let's check if the unit name exists
        # as a key for the dictionary attached
        # to the site_name
        # if it does not already exist, add it
        # and set it to an empty dictionary
        unit_name = sanitized_name(entry['unit_name'])

        if unit_name not in inventory_dictionary['all']['children'][site_name]:
            inventory_dictionary['all']['children'][site_name][unit_name] = {}

        # Finally, let's check if the device_type
        # attached to the unit_name
        # exists as a key for the dictionary
        # if it does not already exist, add it
        # and set it to an empty ARRAY
        expanded_device_type = expanded_name(entry['device_type'], device_types_map)
        device_type = sanitized_name(expanded_device_type)

        if device_type not in inventory_dictionary['all']['children'][site_name][unit_name]:
            inventory_dictionary['all']['children'][site_name][unit_name][device_type] = []

        # Now, let's put the device in the correct place 
        # in the dictionary - under the correct site name,
        # correct unit name, and correct device type

        # First, we format it
        formatted_individual_device = {
            entry['host_name']: {
                'ansible_host': entry['ipv4_address']
            }
        }

        # Then put it in the correct place in the dictionary
        inventory_dictionary['all']['children'][site_name][unit_name][device_type].append(formatted_individual_device)

    return inventory_dictionary


contents = file_contents('./tmp/hosts')
site_names = site_names_map('./mappings/sites.json')
device_types = device_types_map('./mappings/devices.json')

output = formatted_hosts_json(contents, site_names, device_types)
yaml_file = open('output.yaml', 'w+')
yaml.dump(output, yaml_file)
