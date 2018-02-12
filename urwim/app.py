#!/usr/bin/env python3

import asyncio
import logging
import signal
import threading
import urwid

from .command_handler import *
from .command_panel import *
from .input_state_machine import *
from .rdb import *
from .window import *

class App:

    _instance = None

    class _App(urwid.MainLoop):
        def __init__(self, widget, commands=None, keys_mapping=None, command_mapping={}, palette=None):
            widget = widget if widget else urwid.ListBox([])
            self._hack_urwid_asyncio()
            self._draw_lock = threading.RLock()
            self._event_loop = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
            self._command_handler = CommandHandler(commands, command_mapping)
            self._command_panel = CommandPanel(self._command_handler)
            self._window = Window(widget, self._command_panel)
            self._sm = InputStateMachine(keys_mapping)
            self.logger = logging.getLogger('App')
            super().__init__(self._window,
                palette=palette,
                unhandled_input=self._handle_input,
                event_loop=self._event_loop,
                screen=self._create_screen(256))

        def _hack_urwid_asyncio(self):
            # For lower idle CPU usage
            urwid.AsyncioEventLoop._idle_emulation_delay = 1.0/60

        def _create_screen(self, colors):
            screen = urwid.raw_display.Screen()
            try:
                screen.set_terminal_properties(colors)
            except Exception as e:
                self.logger.warning('Cannot setup {} colors: {}'.format(colors, str(e)))
            return screen

        def _handle_input(self, key):
            try:
                if not isinstance(key, tuple):
                    if self._sm.handle_key(key): return
                self._window.handle_input(key)
            except urwid.ExitMainLoop:
                raise
            except Exception as e:
                self._command_panel.error(str(e))

        def draw_screen(self, *args, **kwargs):
            with self.draw_lock:
                super().draw_screen(*args, **kwargs)

        @property
        def command_handler(self):
            return self._command_handler

        @property
        def command_panel(self):
            return self._command_panel

        @property
        def window(self):
            return self._window

        @property
        def draw_lock(self):
            return self._draw_lock

        @property
        def loop(self):
            return self._event_loop

        def run(self):
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            AsyncCaller(self._command_panel.error)
            self.logger.info('Running')
            super().run()

        def quit(self):
            self.logger.info('Exitting')
            raise urwid.ExitMainLoop()

    def __new__(a, *args, **kwargs):
        if App._instance is None:
            App._instance = App._App(*args, **kwargs)
        return App._instance

