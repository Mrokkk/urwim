#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock

import urwim.command_panel
import urwim.pdb

class CommandPanelTests(TestCase):

    def setUp(self):
        self.command_handler_mock = Mock()
        self.command_handler_mock.list_commands.return_value = []
        self.return_focus_callback_mock = Mock()
        urwim.pdb['cmd_history'] = {}
        self.sut = urwim.CommandPanel(self.command_handler_mock)
        self.sut.set_edit_text = Mock()
        self.sut.set_caption = Mock()
        self.sut.set_edit_pos = Mock()
        self.sut.get_edit_text = Mock()

    def activate_and_call(self, command):
        self.sut.activate(':')
        self.sut.get_edit_text.return_value = command
        self.sut.handle_input('enter', self.return_focus_callback_mock)

    def reset_mocks(self):
        self.sut.set_edit_text.reset_mock()
        self.sut.set_caption.reset_mock()

    def test_can_clear_view(self):
        self.sut.clear()
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with('')

    def test_can_display_error(self):
        self.sut.error('Some error')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with(('error', 'Error: Some error'))

    def test_can_display_info(self):
        self.sut.info('Some info')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with(('info', 'Info: Some info'))

    def test_can_be_activated(self):
        self.sut.activate(':')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with(':')

    def test_can_call_command(self):
        self.sut.activate(':')
        self.sut.get_edit_text.return_value = 'command'
        self.sut.handle_input('enter', self.return_focus_callback_mock)
        self.command_handler_mock.assert_called_once_with('command')

    def test_can_exit(self):
        self.sut.activate(':')
        self.sut.handle_input('esc', self.return_focus_callback_mock)
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with('')
        self.return_focus_callback_mock.assert_called_once()

    def test_displays_nothing_when_no_items_in_history(self):
        self.sut.activate(':')
        self.reset_mocks()
        self.sut.handle_input('up', self.return_focus_callback_mock)
        self.sut.set_edit_text.assert_not_called()

        self.sut.activate(':')
        self.reset_mocks()
        self.sut.handle_input('down', self.return_focus_callback_mock)
        self.sut.set_edit_text.assert_not_called()

        self.return_focus_callback_mock.assert_not_called()

    def test_can_display_previous_history_entry(self):
        self.activate_and_call('command1')
        self.sut.activate(':')
        self.reset_mocks()
        self.sut.handle_input('up', self.return_focus_callback_mock)
        self.sut.set_edit_text.assert_called_once_with('command1')

    def test_displays_none_when_trying_to_see_current_command(self):
        self.activate_and_call('command1')
        self.sut.activate(':')
        self.reset_mocks()
        self.sut.handle_input('up', self.return_focus_callback_mock)
        self.sut.set_edit_text.reset_mock()
        self.sut.set_caption.reset_mock()
        self.sut.handle_input('down', self.return_focus_callback_mock)
        self.sut.set_edit_text.assert_called_once_with('')

    def test_can_display_next_item_in_history(self):
        self.activate_and_call('command1')
        self.activate_and_call('command2')
        self.sut.activate(':')
        self.sut.handle_input('up', self.return_focus_callback_mock)
        self.sut.handle_input('up', self.return_focus_callback_mock)
        self.reset_mocks()
        self.sut.handle_input('down', self.return_focus_callback_mock)
        self.sut.set_edit_text.assert_called_once_with('command2')

    def test_tab_keypress_calls_completer_for_command_mode(self):
        self.sut.completer = Mock()
        self.sut.activate(':')
        self.sut.handle_input('tab', self.return_focus_callback_mock)
        self.sut.completer.complete.assert_called_once()
        self.return_focus_callback_mock.assert_not_called()

    def test_tab_keypress_does_not_call_completer_on_other_modes(self):
        self.sut.completer = Mock()
        self.sut.activate('/')
        self.sut.handle_input('tab', self.return_focus_callback_mock)
        self.sut.completer.complete.assert_not_called()
        self.sut.activate('?')
        self.sut.handle_input('tab', self.return_focus_callback_mock)
        self.sut.completer.complete.assert_not_called()
        self.return_focus_callback_mock.assert_not_called()

    def test_handle_input_ignores_other_keys(self):
        self.sut.activate(':')
        self.sut.handle_input('a', self.return_focus_callback_mock)
        self.sut.handle_input('b', self.return_focus_callback_mock)
        self.return_focus_callback_mock.assert_not_called()

    def test_should_be_selectable_only_when_active(self):
        self.assertFalse(self.sut.selectable())
        self.sut.activate(':')
        self.assertTrue(self.sut.selectable())
        self.sut.handle_input('esc', self.return_focus_callback_mock)
        self.return_focus_callback_mock.assert_called_once()
        self.return_focus_callback_mock.reset_mock()
        self.assertFalse(self.sut.selectable())
        self.sut.activate('/')
        self.assertTrue(self.sut.selectable())
        self.sut.handle_input('esc', self.return_focus_callback_mock)
        self.return_focus_callback_mock.assert_called_once()
        self.return_focus_callback_mock.reset_mock()
        self.assertFalse(self.sut.selectable())
        self.sut.activate('?')
        self.assertTrue(self.sut.selectable())

