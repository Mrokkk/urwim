#!/usr/bin/env python3

import os
import logging
from .helpers import log_exception
from .yaml_config_reader import YamlConfigReader
from .json_config_reader import JsonConfigReader

def _convert_color(color):
    if isinstance(color, int):
        return ''.join(['#', hex(color)[2:].rjust(3, '0')])
    return color


def _create_palette_entry(colors, entry, palette):
    # TODO: add support for other color depth
    name = palette[entry]
    try: fg = _convert_color(name['fg'])
    except: fg = ''
    try: bg = _convert_color(name['bg'])
    except: bg = ''
    return (entry, '', '', '', fg, bg)


def _create_palette(palette):
    color_palette = []
    for name in ('head', 'foot', 'file', 'file_focused', 'dir', 'dir_focused', 'error', 'info', 'separator', 'tab_inactive', 'tab_active'):
        try: color_palette.append(_create_palette_entry(256, name, palette))
        except:
            log_exception(logging)
            color_palette.append((name, '', '', '', '', ''))
    return color_palette


def read_config(config_files=[], defaults={}):
    defaults = {
        'colors': 256,
        'color_palette': [
            ('head', 'yellow', 'black', '', '#a30', ''),
            ('foot', 'light gray', 'black', '', '', 'g11'),
            ('file', 'white', '', '', '#fff', ''),
            ('file_focused', 'white', 'black', '', '#fff', 'g11'),
            ('dir', 'dark green', '', '', '#8a5', ''),
            ('dir_focused', 'dark green', 'black', '', '#8a5', 'g11'),
            ('error', 'dark red', '', '', '#a00', ''),
            ('info', 'dark cyan', '', '', '#06f', ''),
            ('separator', 'black', 'black', '', 'g16', ''),
            ('tab_inactive', '', '', '', '', ''),
            ('tab_active', 'black', 'blue', '', '#000', '#0ad'),
        ]
    }

    class Config:
        def __init__(self, d):
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                   setattr(self, a, [Config(x) if isinstance(x, dict) else self._resolve_user_if_needed(x) for x in b])
                else:
                   setattr(self, a, Config(b) if isinstance(b, dict) else self._resolve_user_if_needed(b))

        def _resolve_user_if_needed(self, string):
            if isinstance(string, str):
                return os.path.expanduser(string)
            return string

        def __repr__(self):
            return str(self.__dict__)

    def _read_config(config_files):
        if not config_files: return
        for config_file in config_files:
            config_file = os.path.expanduser(config_file)
            if not os.path.exists(config_file): continue
            if config_file.endswith('.yml'):
                logging.debug('Reading YAML from {}'.format(config_file))
                return YamlConfigReader().read(config_file)
            elif config_file.endswith('.json'):
                logging.debug('Reading JSON from {}'.format(config_file))
                return JsonConfigReader().read(config_file)

    config_dict = defaults.copy()
    if defaults:
        config_dict.update(defaults)
    config_from_file = _read_config(config_files)
    if config_from_file:
        config_dict.update(config_from_file)
    config = Config(config_dict)
    logging.debug(config)
    # FIXME: make the following more generic
    try: config.color_palette = _create_palette(config_dict['palette'])
    except: config.color_palette = defaults['color_palette']
    return config

