#!/usr/bin/env python3

import asyncio
import logging
import signal
import threading
import urwid

from .asynchronous import *
from .command_handler import *
from .command_panel import *
from .commands import *
from .helpers import *
from .input_state_machine import *
from .pdb import *
from .rdb import *
from .window import *

class App:

    _instance = None

    class _App(urwid.MainLoop):
        def __init__(self, widget, config, commands=None, log_exceptions=False):
            commands = Commands() if commands is None else commands
            commands_mapping = config.commands_mapping.__dict__ if 'commands_mapping' in config else {}
            keys_mapping = config.keys_mapping.__dict__ if 'keys_mapping' in config else {}
            palette = config.color_palette
            self._log_exceptions = log_exceptions
            self._hack_urwid_asyncio()
            self._draw_lock = threading.Lock()
            self._event_loop = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
            self._command_handler = CommandHandler(commands, commands_mapping)
            self._command_panel = CommandPanel(self._command_handler)
            self._window = Window(widget, self._command_panel)
            self._sm = InputStateMachine(keys_mapping)
            self.logger = logging.getLogger('App')
            self.exitting = False
            rdb['config'] = RdbObject(config, readonly=True)
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
                if not isinstance(key, tuple) and not self._command_panel.is_active():
                    if self._sm.handle_key(key): return
                self._window.handle_input(key)
            except urwid.ExitMainLoop:
                raise
            except Exception as e:
                if self._log_exceptions:
                    log_exception(self.logger)
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
            self.exitting = True
            pdb.save()
            raise urwid.ExitMainLoop()

    def __new__(a, *args, **kwargs):
        if App._instance is None:
            App._instance = App._App(*args, **kwargs)
        return App._instance

def redraw():
    app = App._instance
    if app is None: return
    if app.exitting: return
    app.draw_screen()

