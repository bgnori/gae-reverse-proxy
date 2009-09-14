#!/usr/bin/env python

from yaml import load, dump
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import os.path
import sys

dir = sys.argv[1]
f = open(os.path.join(dir, 'crawl.yaml'))

try:
  setting = load(f, Loader=Loader)
finally:
  f.close()

print setting

import urllib2

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', setting['ua'])]
for site in setting['sites']:
  for u in site['url']:
    h = opener.open(u)
    print h.read(100)
    h.close()


