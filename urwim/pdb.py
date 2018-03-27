#!/usr/bin/env python3

import json
import os

class Pdb(dict):

    def __init__(self):
        self._filename = None

    def initialize(self, filename):
        filename = os.path.expanduser(filename)
        self._filename = filename
        if not os.path.exists(filename):
            self.save()
        with open(filename, 'r') as f:
            self.update(json.load(f))

    def save(self):
        if not self._filename: return
        with open(self._filename, 'w') as f:
            json.dump(self, f)

pdb = Pdb()

def read_persistent_data(filename):
    pdb.initialize(filename)

