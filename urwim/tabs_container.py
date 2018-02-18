#!/usr/bin/env python3

import urwid
from .widget import *
from .wrapper import *
from .tabs_panel import *

class TabsContainer(urwid.WidgetPlaceholder, Wrapper, Widget):

    def __init__(self, widget_list):
        self._tabs = widget_list
        self._tabs_panel = TabsPanel(self._tabs)
        super().__init__(
            urwid.Frame(widget_list[0], header=self._tabs_panel if len(widget_list) > 1 else None)
        )

    def add_tab(self, w):
        self._tabs.append(w)
        self._tabs_panel.add_tab(w)
        if len(self._tabs) > 1:
            self.original_widget = urwid.Frame(self._tabs[self._get_current_tab_index()], header=self._tabs_panel)

    def _get_current_tab_index(self):
        for i, w in enumerate(self._tabs):
            if w == self.focus: return i

    def next_tab(self):
        if len(self._tabs) <= 1: return
        current_tab = self._get_current_tab_index()
        try:
            self.original_widget = urwid.Frame(self._tabs[current_tab + 1], header=self._tabs_panel)
            self._tabs_panel.select(current_tab + 1)
        except:
            self.original_widget = urwid.Frame(self._tabs[0], header=self._tabs_panel)
            self._tabs_panel.select(0)

    def prev_tab(self):
        if len(self._tabs) <= 1: return
        current_tab = self._get_current_tab_index()
        new_index = current_tab - 1
        if new_index < 0: new_index = len(self._tabs) - 1
        self.original_widget = urwid.Frame(self._tabs[new_index], header=self._tabs_panel)
        self._tabs_panel.select(new_index)

    def switch_panes(self):
        self.focus.switch_panes()
        tab_index = self._get_current_tab_index()
        self._tabs_panel.update(tab_index)

    def switch_left(self):
        self.focus.switch_left()
        tab_index = self._get_current_tab_index()
        self._tabs_panel.update(tab_index)

    def switch_right(self):
        self.focus.switch_right()
        tab_index = self._get_current_tab_index()
        self._tabs_panel.update(tab_index)

    @property
    def focus(self):
        return self.original_widget.focus

