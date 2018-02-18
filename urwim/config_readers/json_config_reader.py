#!/usr/bin/env python3

import json
import os
import urwid

class JsonConfigReader:

    def read(self, path):
        try:
            with open(os.path.expanduser(path), 'r') as f:
                return json.loads(f.read())
        except:
            pass

