#!/usr/bin/env python3

import urwid
from .tabs_container import *
from .vertical_box import *
from .wrapper import *

class Window(urwid.WidgetWrap, Wrapper):

    def __init__(self, main_view, command_panel):
        self.main_view = main_view if main_view else urwid.ListBox([])
        self._command_panel = command_panel
        self._tabs_container = TabsContainer([main_view])
        super().__init__(urwid.Frame(self._tabs_container, footer=self._command_panel))

    def add_tab(self, w):
        self._tabs_container.add_tab(w)

    def next_tab(self):
        self._tabs_container.next_tab()

    def prev_tab(self):
        self._tabs_container.prev_tab()

    def keypress(self, size, key):
        if key in self._command_panel.activation_keys and not self._command_panel.is_active():
            self._focus_command_panel()
            self._command_panel.activate(key)
            return None
        return super().keypress(size, key)

    def handle_input(self, key):
        if self._w.focus_position == 'footer':
            return self._command_panel.handle_input(key, self._focus_body)
        self._tabs_container.handle_input(key)

    def _focus_command_panel(self):
        self._w.focus_position = 'footer'

    def _focus_body(self):
        self._w.focus_position = 'body'

    @property
    def focus(self):
        return self._tabs_container

