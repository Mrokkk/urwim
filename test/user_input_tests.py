#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from urwim.input_state_machine import *

class InputStateMachineTests(TestCase):

    def setUp(self):
        self.view_mock = Mock()
        self.command_handler_mock = Mock()
        self.command_panel_mock = Mock()
        self.error_handler_mock = Mock()
        self.command_panel_mock.activation_keys = [':', '/', '?']
        self.command_panel_mock.error = self.error_handler_mock
        self.context = Mock()
        self.context.command_handler = self.command_handler_mock
        self.context.command_panel = self.command_panel_mock
        self.context.window = self.view_mock
        self.context.event_loop = MagicMock()
        self.sut = InputStateMachine(self.context)
        self.sut.key_to_command_mapping = {}

    # FIXME
    # def test_can_handle_not_mapped_key(self):
        # self.view_mock.handle_input.return_value = True
        # self.sut.handle_input('a')
        # self.view_mock.handle_input.assert_called_once_with('a')

    # def test_can_handle_not_mapped_key_and_change_focus(self):
        # self.view_mock.handle_input.return_value = False
        # self.sut.handle_input('a')
        # self.view_mock.handle_input.assert_called_once_with('a')

    # def test_can_handle_mapped_key(self):
        # self.sut.handle_input('h')
        # self.command_handler_mock.assert_called_once_with(':seek -10')
        # self.context.event_loop.alarm.assert_not_called()

    # def test_can_handle_keys_sequence(self):
        # self.sut.handle_input('g')
        # self.context.event_loop.alarm.assert_called_once()
        # self.sut.handle_input('g')
        # self.context.event_loop.remove_alarm.assert_called_once()
        # self.context.window.focus.searchable_list.assert_called_once()

    # def test_can_handle_break_keys_sequence(self):
        # self.sut.handle_input('g')
        # self.context.event_loop.alarm.assert_called_once()
        # self.sut.handle_input('esc')
        # self.context.event_loop.remove_alarm.assert_called_once()
        # self.context.window.focus.searchable_list.assert_not_called()

    # def test_can_handle_mouse_press(self):
        # self.sut.handle_input(('mouse press', 1))
        # self.context.event_loop.alarm.assert_not_called()
        # self.context.window.focus.searchable_list.assert_not_called()
        # self.view_mock.handle_input.assert_called_once_with(('mouse press', 1))

