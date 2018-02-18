#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from urwim import read_config

class ConfigTests(TestCase):

    def test_can_read_simple_config(self):
        config = {
            'backend': {
                'name': 'some_backend',
                'path': '/path/to/some_backend'
            }
        }
        with patch('builtins.open') as open_mock, \
                patch('yaml.load') as yaml_load_mock, \
                patch('os.path.exists') as exists_mock:
            yaml_load_mock.return_value = config
            exists_mock.return_value = True
            sut = read_config(config_files=['some_file.yml'])
            open_mock.assert_called_once()
            yaml_load_mock.assert_called_once()
            self.assertEqual(sut.backend.name, 'some_backend')
            self.assertEqual(sut.backend.path, '/path/to/some_backend')

