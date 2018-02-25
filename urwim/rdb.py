#!/usr/bin/env python3

import logging

class RdbObject:

    def __init__(self, value, min_value=None, max_value=None, readonly=False):
        self._value = value
        self._min = min_value
        self._max = max_value
        self._readonly = readonly

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._readonly: raise RuntimeError('this object is readonly')
        if self._min is not None:
            if value < self._min: raise RuntimeError('exceeded constraints')
        if self._max is not None:
            if value > self._max: raise RuntimeError('exceeded constraints')
        self._value = value


class Rdb(dict):

    def __init__(self):
        super().__init__()
        self._subscriptions = {}
        self.logger = logging.getLogger('Rdb')

    def __getitem__(self, key):
        return super().__getitem__(key).value

    def _handle_change(self, key, old, new):
        if isinstance(old, RdbObject): old = old.value
        if isinstance(new, RdbObject): new = new.value
        self.logger.debug('{}: {} -> {}'.format(key, old, new))
        if key in self._subscriptions:
            for sub in self._subscriptions[key]:
                sub(new)

    def __setitem__(self, key, value):
        try:
            old_value = super().__getitem__(key)
        except: old_value = None
        if old_value == None:
            if not isinstance(value, RdbObject):
                value = RdbObject(value)
            super().__setitem__(key, value)
        else:
            if isinstance(value, RdbObject):
                super().__setitem__(key, value)
            else:
                old_value.value = value
        self._handle_change(key, old_value, value)

    def subscribe(self, key, callback):
        if key not in self:
            super().__setitem__(key, None)
        if key not in self._subscriptions:
            self._subscriptions[key] = []
        self._subscriptions[key].append(callback)

rdb = Rdb()

