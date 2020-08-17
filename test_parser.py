#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest.mock import patch, mock_open
import json
import unittest
import parser
import re
import pprint

print(reader())

class TestRegex(unittest.TestCase):
    def test_parser(self):
        pp = pprint.PrettyPrinter(indent=1)
        print(reader())
        
if __name__ == '__main__':
    unittest.main()