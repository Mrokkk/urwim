#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from urwim.completer import *

class CompleterTests(TestCase):

    def setUp(self):
        self.command_panel_mock = Mock()
        self.commands = ['add_to_playlist', 'e', 'load_playlist', 'next', 'pause', 'prev', 'q', 'qa', 'quit', 'save_playlist', 'seek', 'set', 'stop', 'switch_panes']
        self.sut = Completer(self.commands, self.command_panel_mock)

    def test_can_get_first_completion_if_command_panel_is_empty(self):
        self.command_panel_mock.get_edit_text.return_value = ''
        self.sut.complete(None)
        self.command_panel_mock.insert_text.assert_called_once_with('add_to_playlist')

    def test_can_complete_with_first_matched_command(self):
        self.command_panel_mock.get_edit_text.return_value = 'p'
        self.sut.complete(None)
        self.command_panel_mock.insert_text.assert_called_once_with('ause')

    def test_can_complete_next_matched_command(self):
        self.command_panel_mock.get_edit_text.return_value = 'p'
        context = self.sut.complete(None)
        self.command_panel_mock.insert_text.assert_called_once_with('ause')
        self.command_panel_mock.insert_text.reset_mock()
        self.command_panel_mock.get_edit_text.return_value = 'pause'
        context = self.sut.complete(context)
        self.command_panel_mock.set_edit_text.assert_called_once_with('prev')
        self.command_panel_mock.set_edit_text.reset_mock()
        self.command_panel_mock.get_edit_text.return_value = 'prev'
        context = self.sut.complete(context)
        self.command_panel_mock.set_edit_text.assert_called_once_with('pause')

    def test_changing_edit_text_invalidates_completer_context(self):
        self.command_panel_mock.get_edit_text.return_value = 's'
        context1 = self.sut.complete(None)
        self.command_panel_mock.insert_text.assert_called_once_with('ave_playlist')
        self.command_panel_mock.insert_text.reset_mock()
        self.command_panel_mock.get_edit_text.return_value = 'se'
        context2 = self.sut.complete(context1)
        self.assertNotEqual(context1, context2)
        self.command_panel_mock.insert_text.assert_called_once_with('ek')
        self.command_panel_mock.insert_text.reset_mock()

    def test_does_nothing_when_no_matched_command_found(self):
        self.command_panel_mock.get_edit_text.return_value = 'aaa'
        context = self.sut.complete(None)
        self.assertEqual(context, None)
        self.command_panel_mock.insert_text.assert_not_called()
        self.command_panel_mock.set_edit_text.assert_not_called()

    def test_can_complete_first_argument(self):
        self.command_panel_mock.get_edit_text.return_value = 'save_playlist '
        with patch('os.listdir') as listdir_mock:
            listdir_mock.return_value = ['file2', 'file1']
            context = self.sut.complete(None)
            self.command_panel_mock.insert_text.assert_called_once_with('file1')
            self.command_panel_mock.insert_text.reset_mock()
            self.command_panel_mock.get_edit_text.return_value = 'save_playlist file1'
            context = self.sut.complete(context)
            self.command_panel_mock.set_edit_text.assert_called_once_with('save_playlist file2')
            self.command_panel_mock.set_edit_text.reset_mock()
            self.command_panel_mock.get_edit_text.return_value = 'save_playlist file2'
            context = self.sut.complete(context)
            self.command_panel_mock.set_edit_text.assert_called_once_with('save_playlist file1')
            self.command_panel_mock.set_edit_text.reset_mock()
            self.command_panel_mock.get_edit_text.return_value = 'save_playlist e'
            context = self.sut.complete(context)
            self.assertEqual(context, None)
            self.command_panel_mock.set_edit_text.assert_not_called()

    def test_can_complete_first_argument_2(self):
        self.command_panel_mock.get_edit_text.return_value = 'save'
        with patch('os.listdir') as listdir_mock:
            listdir_mock.return_value = ['file2', 'file1']
            context = self.sut.complete(None)
            self.command_panel_mock.insert_text.assert_called_once_with('_playlist')
            self.command_panel_mock.insert_text.reset_mock()
            self.command_panel_mock.get_edit_text.return_value = 'save_playlist '
            context = self.sut.complete(context)
            self.command_panel_mock.insert_text.assert_called_once_with('file1')
            self.command_panel_mock.insert_text.reset_mock()
            self.command_panel_mock.get_edit_text.return_value = 'save_playlist file1'
            context = self.sut.complete(context)
            self.command_panel_mock.set_edit_text.assert_called_once_with('save_playlist file2')
            self.command_panel_mock.set_edit_text.reset_mock()
            self.command_panel_mock.get_edit_text.return_value = 'save_playlist e'
            context = self.sut.complete(context)
            self.assertEqual(context, None)
            self.command_panel_mock.set_edit_text.assert_not_called()

