#!/usr/bin/env python3

import re
import urwim.app

class InputStateMachine:

    def __init__(self, keys_mapping):
        self._keys = {
            'gg': lambda: urwim.App().window.searchable_list().scroll_beginning(),
            'G': lambda: urwim.App().window.searchable_list().scroll_end(),
            'dd': lambda: urwim.App().window.searchable_list().delete(),
            '<C-w>left': lambda: urwim.App().window.switch_left(),
            '<C-w>right': lambda: urwim.App().window.switch_right(),
            '<C-w><C-w>': lambda: urwim.App().window.switch_panes(),
            'b': lambda: urwim.App().window.toggle_pane_view(),
            ',h': lambda: urwim.App().window.prev_tab(),
            ',l': lambda: urwim.App().window.next_tab(),
            'n': lambda: urwim.App().command_handler('/'),
            'N': lambda: urwim.App().command_handler('?'),
        }
        if keys_mapping is not None:
            for k, v in keys_mapping.items():
                self._keys[k] = lambda v=v: urwim.App().command_handler(v)
        self._state = ''
        self._alarm = None

    def _clear(self):
        if self._alarm: urwim.App().loop.remove_alarm(self._alarm)
        self._state = ''
        self._alarm = None

    def _convert_key(self, key):
        if 'meta' in key:
            return re.sub(r'meta (.)', r'<M-\1>', key)
        elif 'ctrl' in key:
            return re.sub(r'ctrl (.)', r'<C-\1>', key)
        return key

    def handle_key(self, key):
        key = self._convert_key(key)
        if key == 'esc':
            self._clear()
            return False
        self._state = ''.join([self._state, key])
        for k in self._keys:
            if self._state == k:
                self._keys[self._state]()
                self._clear()
                return True
            elif k.startswith(self._state):
                self._alarm = urwim.App().loop.alarm(1, self._clear)
                return True
        self._clear()
        return False

