#!/usr/bin/env python3

import urwid
from .helpers import *
from .widget import *

class ListWidget(urwid.ListBox, Widget):

    def __init__(self, content, readonly=False):
        self._readonly = readonly
        super().__init__(content)

    def _try_to_scroll(self, key):
        try:
            if key == 5.0:
                if not self.body[self.focus_position + 1].selectable(): return
                self.focus_position += 1
                return True
            elif key == 4.0:
                if not self.body[self.focus_position - 1].selectable(): return
                self.focus_position -= 1
                return True
        except: pass

    def mouse_event(self, size, event, button, col, row, focus):
        if self._try_to_scroll(button): return None
        return super().mouse_event(size, event, button, col, row, focus)

    def keypress(self, size, key):
        if key == 'home':
            # FIXME: check if element is selectable
            self.scroll_beginning()
            return None
        elif key == 'end':
            self.scroll_end()
            return None
        return super().keypress(size, key)

    def scroll_beginning(self):
        self.focus_position = 0

    def scroll_end(self):
        self.focus_position = len(self.body) - 1

    def search_forward(self, pattern):
        index = self.focus_position + 1
        while True:
            try:
                if pattern in self.body[index].text:
                    self.focus_position = index
                    return
                index += 1
            except:
                break

    def search_backward(self, pattern):
        index = self.focus_position - 1
        while True:
            try:
                if pattern in self.body[index].text:
                    self.focus_position = index
                    return
                index -= 1
                if index < 0: return
            except:
                break

    def readonly(self):
        return self._readonly

    def delete(self):
        if self.readonly(): raise RuntimeError('this widget does not support removing items')
        del self.body[self.focus_position]

    def searchable_list(self):
        return self

