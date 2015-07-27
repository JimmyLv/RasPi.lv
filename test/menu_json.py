#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import json

data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23
}

json_str = json.dumps(data)
print json_str

# Reading data back
with open('../menu.json', 'r') as f:
    menu_data = json.load(f)
print menu_data
