#!/usr/bin/env python3

import urwid

class Header(urwid.WidgetWrap):

    signals = []

    def __init__(self, name):
        self._name = name
        super().__init__(urwid.AttrWrap(urwid.Text(self._name), 'head'))

    @property
    def text(self):
        return self._name

    @text.setter
    def text(self, text):
        self._name = text
        self._w = urwid.AttrWrap(urwid.Text(self._name), 'head')

