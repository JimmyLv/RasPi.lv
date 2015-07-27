#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import dhtreader

dhtreader.init()

print dhtreader.read(11, 4)

t, h = dhtreader.read(11, 4)

print t
print h