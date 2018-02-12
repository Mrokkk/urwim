#!/usr/bin/env python3

import os
import urwid
import yaml

class YamlConfigReader:

    def read(self, path):
        try:
            with open(os.path.expanduser(path), 'r') as f:
                return yaml.load(f.read())
        except:
            pass

