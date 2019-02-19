#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, patch

class CommandHandlerTests(TestCase):

    def setUp(self):
        self.command_handler_mock = Mock()
        self.command_panel_mock = Mock()
        self.window_mock = Mock()
        self.app_instance = Mock()
        self.app_instance.command_handler = self.command_handler_mock
        self.app_instance.command_panel = self.command_panel_mock
        self.app_instance.window = self.window_mock
        self.app_mock = Mock()
        self.app_mock.return_value = self.app_instance

        patch('urwim.asynchronous', lambda x: x).start()
        patch('urwim.App', self.app_mock).start()
        patch('urwim.app.App', self.app_mock).start()
        import urwim.commands
        import urwim.command_handler
        self.commands = urwim.commands.Commands()
        self.sut = urwim.command_handler.CommandHandler(self.commands, {})


    def test_can_execute_player_controller_commands(self):
        self.sut(':quit')
        self.app_instance.quit.assert_called_once()


    def test_can_execute_view_commands(self):
        self.sut(':switch_panes')
        self.window_mock.switch_panes.assert_called_once()

        self.sut(':toggle_pane_view')
        self.window_mock.toggle_pane_view.assert_called_once()


    def test_bad_command_shows_error(self):
        bad_commands = [':plya', ':run', ':start', ':spot', '::', 'aa']
        for cmd in bad_commands:
            self.sut(cmd)
            self.command_panel_mock.error.assert_called_once()
            self.command_panel_mock.error.reset_mock()


    def test_can_seek_forward(self):
        list_mock = Mock()
        self.window_mock.searchable_list.return_value = list_mock
        self.sut('/some_string')
        list_mock.search_forward.assert_called_once_with('some_string')


    def test_can_seek_forward_same_string(self):
        list_mock = Mock()
        self.window_mock.searchable_list.return_value = list_mock
        self.sut('/some_string')
        list_mock.search_forward.assert_called_once_with('some_string')
        list_mock.search_forward.reset_mock()
        self.sut('/')
        list_mock.search_forward.assert_called_once_with('some_string')


    def test_can_seek_backward(self):
        list_mock = Mock()
        self.window_mock.searchable_list.return_value = list_mock
        self.sut('?some_string')
        list_mock.search_backward.assert_called_once_with('some_string')


    def test_can_seek_forward_same_string(self):
        list_mock = Mock()
        self.window_mock.searchable_list.return_value = list_mock
        self.sut('?some_string')
        list_mock.search_backward.assert_called_once_with('some_string')
        list_mock.search_backward.reset_mock()
        self.sut('?')
        list_mock.search_backward.assert_called_once_with('some_string')


    def test_should_do_nothing_when_trying_to_seek_last_keyword_but_there_was_no_search(self):
        list_mock = Mock()
        self.window_mock.searchable_list.return_value = list_mock
        self.sut('?')
        self.sut('/')
        list_mock.search_backward.assert_not_called()
        list_mock.search_forward.assert_not_called()


    def test_can_call_mapped_commands(self):
        self.sut(':q')
        self.app_instance.quit.assert_called_once()


    def test_ignores_empty_command(self):
        self.sut('')
        self.command_panel_mock.error.assert_not_called()


    def test_cannot_set_bad_key(self):
        self.sut(':set aaakkkk value')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()
        self.sut(':set key value')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()
        self.sut(':set vcbx value')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()


    def test_cannot_get_bad_key(self):
        self.sut(':get aaakkk')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()
        self.sut(':get key')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()
        self.sut(':get vcbx')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()


    def test_can_properly_list_commands(self):
        commands = self.sut.list_commands()
        bad_commands = [x for x in commands if x.startswith('_')]
        self.assertEqual(len(bad_commands), 0)
        self.assertGreater(len(commands), 0)

