#!/usr/bin/env python3

import urwid
from .widget import *

class ViewWidget(urwid.Frame, Widget):

    def __init__(self, widget, name, callbacks={}, header=None):
        self._callbacks = callbacks
        self._widget = widget
        self._name = name
        super().__init__(widget, header=header)

    def handle_input(self, key):
        if key in self._callbacks:
            self._callbacks[key]()

    def searchable_list(self):
        return self._widget.searchable_list()

    @property
    def name(self):
        return self._name

