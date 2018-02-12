#!/usr/bin/env python3

import urwid

class HorizontalSeparator(tuple):

    def __new__(self):
        return (1, urwid.AttrWrap(urwid.SolidFill('-'), 'separator'))


class VerticalSeparator(tuple):

    def __new__(self):
        return (1, urwid.AttrWrap(urwid.SolidFill('|'), 'separator'))

