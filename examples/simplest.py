#!/usr/bin/env python3

import os
import sys
sys.path.insert(1, os.path.abspath(os.path.dirname(sys.argv[0])) + '/..')
import urwim

def main():
    urwim.App(None, urwim.read_config()).run()

if __name__ == '__main__':
    main()

