#!/usr/bin/env python3

import enum
import logging
import shlex
import urwid
import urwim.app
from .asynchronous import *
from .commands import *

class CommandHandler:

    class Mode(enum.Enum):
        COMMAND = ':'
        SEARCH_FORWARD = '/'
        SEARCH_BACKWARD = '?'

    def __init__(self, commands, command_mapping):
        self.commands = commands if commands else Commands()
        self.mode_map = {
            self.Mode.COMMAND: self._command_mode,
            self.Mode.SEARCH_FORWARD: lambda c: self._search_forward_mode(c),
            self.Mode.SEARCH_BACKWARD: lambda c: self._search_backward_mode(c)
        }
        self.command_mapping = {
            'q': 'quit',
            'qa': 'quit',
            **command_mapping
        }
        self.logger = logging.getLogger('CommandHandler')
        self._search_context = None

    def _format_arguments(self, args):
        if len(args) == 0: return ''
        return ','.join('\'{}\''.format(arg.strip().replace('\'', '\\\'')) for arg in args)

    def _command_mode(self, command):
        splitted = shlex.split(command)
        command = splitted[0]
        args = splitted[1:]
        if command in self.command_mapping:
            command = self.command_mapping[command]
        if not hasattr(self.commands, command):
            raise RuntimeError('no such command: ' + command)
        eval('self.commands.{}({})'.format(command, self._format_arguments(args)))

    def _search_forward_mode(self, command):
        urwim.App().window.searchable_list().search_forward(command)

    def _search_backward_mode(self, command):
        urwim.App().window.searchable_list().search_backward(command)

    def list_commands(self):
        import inspect
        commands = [x[0] for x in inspect.getmembers(self.commands, predicate=inspect.ismethod) if not x[0].startswith('_')]
        commands.extend(self.command_mapping.keys())
        return commands

    def __call__(self, command):
        if not command: return
        try: mode = [e for e in self.Mode if e.value == command[0]][0]
        except IndexError:
            self.commands.error('bad mode')
            return
        try: self.mode_map[mode](command[1:])
        except urwid.ExitMainLoop:
            raise
        except Exception as exc:
            self.commands.error(str(exc))

