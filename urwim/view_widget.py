#!/usr/bin/env python3

import urwid
from .list_widget import *

class ViewWidget(urwid.Frame):

    def __init__(self, widget, callbacks, name, header=None):
        self._callbacks = callbacks
        self._widget = widget
        self._name = name
        super().__init__(widget, header=header)

    def handle_input(self, key):
        if key in self._callbacks:
            self._callbacks[key]()

    def searchable_list(self):
        if self._widget.__class__ == ListWidget: return self._widget
        raise NotImplementedError('view does not support searching')

    @property
    def name(self):
        return self._name

