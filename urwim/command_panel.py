#!/usr/bin/env python3

import urwid
from .helpers import clamp
from .completer import *

class CommandPanel(urwid.Edit):

    def __init__(self, command_handler):
        super().__init__()
        self.command_handler = command_handler
        self.mode = None
        self.history_index = None
        self.activation_keys = (':', '/', '?')
        self.history = {
            self.activation_keys[0]: [],
            self.activation_keys[1]: [],
            self.activation_keys[2]: [],
        }
        self.history_index = -1
        self.completer = Completer(self.command_handler.list_commands(), self)
        self.completer_context = None

    def _clear_and_set_caption(self, caption):
        self.set_edit_text('')
        self.set_caption(caption)

    def is_active(self):
        return self.mode != None

    def activate(self, key):
        self.mode = key
        self._clear_and_set_caption(key)
        self.history_index = -1

    def deactivate(self):
        self.mode = None

    def error(self, error):
        self._clear_and_set_caption(('error', 'Error: ' + error))
        self.deactivate()

    def info(self, error):
        self._clear_and_set_caption(('info', 'Info: ' + error))
        self.deactivate()

    def clear(self):
        self._clear_and_set_caption('')
        self.deactivate()

    def _update_panel(self):
        self.set_edit_text(self.history[self.mode][self.history_index])
        self.set_edit_pos(len(self.edit_text))

    def _handle_enter(self):
        self.history[self.mode].insert(0, self.get_edit_text().strip())
        self.command_handler(self.caption + self.get_edit_text().strip())
        if self.is_active(): self.clear()

    def _handle_up_arrow(self):
        try:
            self.history_index += 1
            self.history_index = clamp(self.history_index, max_val=len(self.history[self.mode])-1)
            self._update_panel()
        except: pass
        return True

    def _handle_down_arrow(self):
        if self.history_index < 0: return True
        self.history_index -= 1
        self.history_index = clamp(self.history_index, min_val=-1)
        if self.history_index == -1:
            self.set_edit_text('')
            self.set_edit_pos(0)
            return True
        self._update_panel()
        return True

    def selectable(self):
        return self.mode != None

    def handle_input(self, key, return_focus_callback):
        if key == 'enter':
            self._handle_enter()
            return_focus_callback()
        elif key == 'esc':
            self.clear()
            return_focus_callback()
        elif key == 'up':
            self._handle_up_arrow()
        elif key == 'down':
            self._handle_down_arrow()
        elif key == 'tab':
            if self.mode == ':':
                self.completer_context = self.completer.complete(self.completer_context)

