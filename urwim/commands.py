#!/usr/bin/env python3

import urwim.app
import urwim.rdb

class Commands:

    def error(self, string):
        urwim.App().command_panel.error(string)

    def info(self, string):
        urwim.App().command_panel.info(string)

    def switch_panes(self):
        urwim.App().window.switch_panes()

    def toggle_pane_view(self):
        urwim.App().window.toggle_pane_view()

    def quit(self):
        urwim.App().quit()

    def get(self, key):
        value = urwim.rdb[key]
        self.info('{}: {}'.format(key, value))
        return value

    def set(self, key, value):
        old_value = urwim.rdb[key]
        if '+' in value:
            new_value = old_value + int(value[1:])
        elif '-' in value:
            new_value = old_value - int(value[1:])
        else:
            new_value = int(value)
        urwim.rdb[key] = new_value

    def tabnew(self):
        raise NotImplementedError('not implemented')

    def tabn(self):
        urwim.App().window.next_tab()

    def tabp(self):
        urwim.App().window.prev_tab()

