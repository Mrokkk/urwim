#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, patch
from urwim.rdb import *

class RdbTests(TestCase):

    def setUp(self):
        self.sut = Rdb()


    def test_can_write_some_data(self):
        self.sut['aaa'] = 'bbb'
        self.assertEqual(self.sut['aaa'], 'bbb')


    def test_can_subscribe(self):
        self.sut['aaa'] = 'bbb'
        callback_mock = Mock()
        self.sut.subscribe('aaa', callback_mock)
        self.sut['aaa'] = 'ccc'
        callback_mock.assert_called_once_with('ccc')

        callback_mock.reset_mock()
        self.sut.subscribe('ddd', callback_mock)
        self.sut['ddd'] = 'ggg'
        callback_mock.assert_called_once_with('ggg')

