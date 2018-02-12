#!/usr/bin/env python3

import logging
import urwid
from .footer import *
from .helpers import *
from .separators import *
from .wrapper import *

class VerticalBox(urwid.WidgetPlaceholder, Wrapper):

    def __init__(self, widget_list):
        self._widgets = []
        super().__init__(urwid.Columns(urwid.ListBox([])))
        self._toggle_callbacks = []
        for w in widget_list:
            self.add_pane(w)

    def keypress(self, size, key):
        if key == 'right' or key == 'left': return key
        return super().keypress(size, key)

    def _toggle_view(self, widget_list):
        for i, widget in enumerate(widget_list):
            if self.focus == widget:
                try:
                    self.original_widget.focus.original_widget = urwid.Frame(
                        widget_list[i + 1],
                        footer=Footer(widget_list[i + 1].name))
                except:
                    self.original_widget.focus.original_widget = urwid.Frame(
                        widget_list[0],
                        footer=Footer(widget_list[0].name))
                return True

    def toggle_pane_view(self):
        for c in self._toggle_callbacks:
            if c(): return

    def _wrap_widget(self, w):
        if isinstance(w, list):
            widget = w[0]
            self._toggle_callbacks.append(lambda: self._toggle_view(w))
        else:
            widget = w
        widget_name = widget.name
        return urwid.WidgetPlaceholder(urwid.Frame(widget, footer=Footer(widget_name)))

    def add_pane(self, widget):
        current = self.original_widget.focus
        new_widgets = []
        if current == None:
            new_widgets.append(self._wrap_widget(widget))
        else:
            for w in self._widgets:
                new_widgets.append(w)
                if w == current:
                    new_widgets.append(VerticalSeparator())
                    new_widgets.append(self._wrap_widget(widget))
        self._widgets = new_widgets
        self.original_widget = urwid.Columns(self._widgets)

    def handle_input(self, key):
        widget = self.focus
        if isinstance(widget, urwid.WidgetPlaceholder):
            widget.original_widget.handle_input(key)
        else:
            widget.handle_input(key)

    def switch_panes(self):
        current_position = self.focus_position
        try:
            self.original_widget.set_focus(current_position + 2)
        except:
            self.original_widget.set_focus(0)

    def switch_left(self):
        current_position = self.focus_position
        try:
            self.original_widget.set_focus(current_position - 2)
        except:
            pass

    def switch_right(self):
        current_position = self.focus_position
        try:
            self.original_widget.set_focus(current_position + 2)
        except:
            pass

    @property
    def focus(self):
        return self.original_widget.focus.original_widget.contents['body'][0]

    @property
    def focus_position(self):
        return self.original_widget.focus_position

    @focus_position.setter
    def focus_position(self, index):
        self.original_widget.set_focus(index * 2)

    def __getitem__(self, index):
        return self._widget_list[index * 2]

