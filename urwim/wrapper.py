#!/usr/bin/env python3

class Wrapper:

    def handle_input(self, key):
        self.focus.handle_input(key)

    def toggle_pane_view(self):
        self.focus.toggle_pane_view()

    def switch_panes(self):
        self.focus.switch_panes()

    def switch_left(self):
        self.focus.switch_left()

    def switch_right(self):
        self.focus.switch_right()

    def searchable_list(self):
        return self.focus.searchable_list()

    @property
    def name(self):
        return self.focus.name

