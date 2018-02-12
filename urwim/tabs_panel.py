#!/usr/bin/env python3

import urwid

class TabsPanel(urwid.WidgetWrap):

    class Tab(urwid.WidgetWrap):
        def __init__(self, index, name, active=False):
            super().__init__(urwid.AttrMap(
                urwid.Text(' {} {} '.format(index, name)), 'tab_active' if active else 'tab_inactive'
            ))


    def __init__(self, tabs):
        self._tabs = tabs
        super().__init__(urwid.Columns([], dividechars=1))
        for i, t in enumerate(tabs):
            self.add_tab(t, selected=i==0)

    def add_tab(self, tab, selected=False):
        self._w.contents.append((
            self.Tab(len(self._w.contents) + 1, tab.name, active=selected),
            self._w.options('pack')
        ))

    def select(self, index):
        for i, t in enumerate(self._tabs):
            if index == i:
                self._w.contents[i] = (
                    self.Tab(index + 1, self._tabs[index].name, active=True),
                    self._w.options('pack')
                )
            else:
                self._w.contents[i] = (
                    self.Tab(index + 1, self._tabs[index].name, active=False),
                    self._w.options('pack')
                )

    def update(self, index):
        self._w.contents[index] = (
            self.Tab(index + 1, self._tabs[index].name, active=True),
            self._w.options('pack')
        )

    def selectable(self):
        return False

