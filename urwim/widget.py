#!/usr/bin/env python3

class Widget:

    def handle_input(self, key):
        raise NotImplementedError('{} does not implement handle_input'.format(self.__class__.__name__))

    def toggle_pane_view(self):
        raise NotImplementedError('{} does not implement toggle_pane_view'.format(self.__class__.__name__))

    def switch_panes(self):
        raise NotImplementedError('{} does not implement switch_panes'.format(self.__class__.__name__))

    def switch_left(self):
        raise NotImplementedError('{} does not implement switch_left'.format(self.__class__.__name__))

    def switch_right(self):
        raise NotImplementedError('{} does not implement switch_right'.format(self.__class__.__name__))

    def searchable_list(self):
        raise NotImplementedError('{} does not implement searchable_list'.format(self.__class__.__name__))

    @property
    def name(self):
        return self.__class__.__name__

