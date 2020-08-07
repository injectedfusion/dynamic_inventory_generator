#! /usr/bin/env python3
import json

with open('sites.json') as f:
    sites = json.load(f)

# Output
print(sites)