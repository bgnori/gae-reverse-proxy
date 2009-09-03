#!/usr/bin/env python

from yaml import load, dump
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper



if __name__ == "__main__":
    import sys
    f = open(sys.argv[1])
    try:
      template = load(f, Loader=Loader)
    finally:
      f.close()

    f = open(sys.argv[2])
    try:
      usr = load(f, Loader=Loader)
    finally:
      f.close()

    template.update(usr)
    print dump(template, default_flow_style=False)
