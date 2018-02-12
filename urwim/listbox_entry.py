#!/usr/bin/env python3

import urwid

class ListBoxEntry(urwid.Button):

    signals = []

    def __init__(self, text, unfocused=None, focused=None):
        super().__init__('')
        self.update(text, unfocused, focused)

    @property
    def text(self):
        '''Has to be implemented by subclass; used for searching in ListBox'''
        raise NotImplementedError('text property not implemented by widget')

    def update(self, text, unfocused=None, focused=None):
        widget = urwid.SelectableIcon(text, 0)
        if unfocused and focused:
            widget = urwid.AttrMap(widget, unfocused, focused)
        self._w = widget

    def keypress(self, size, key):
        '''Ignore key presses'''
        return key

