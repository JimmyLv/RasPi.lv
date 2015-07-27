#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import re
import subprocess

def read_temp(output):
    matches = re.search("Temp =\s+([0-9.]+)", output)
    if (matches):
        return float(matches.group(1))

def read_hum(output):
    matches = re.search("Hum =\s+([0-9.]+)", output)
    if (matches):
        return float(matches.group(1))

while True:
    output = subprocess.check_output("sudo ../Adafruit_DHT 11 4", shell = True)
    print read_temp(output)
    print read_hum(output)
    time.sleep(1)
