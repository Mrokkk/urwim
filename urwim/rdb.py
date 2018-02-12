#!/usr/bin/env python3

import logging

class Value:

    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._vaule = value


class ConstrainedValue(Value):

    def __init__(self, value, min=None, max=None):
        self._min = min
        self._max = max
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if (value < self._min) or (value > self._max):
            raise RuntimeError('exceeded constraints')
        self._value = value


class Rdb(dict):

    def __init__(self):
        super().__init__()
        self._subscriptions = {}
        self.logger = logging.getLogger('Rdb')

    def __getitem__(self, key):
        return super().__getitem__(key).value

    def _handle_change(self, key, old, new):
        if isinstance(old, Value): old = old.value
        if isinstance(new, Value): new = new.value
        self.logger.info('{}: {} -> {}'.format(key, old, new))
        if key in self._subscriptions:
            for sub in self._subscriptions[key]:
                sub(new)

    def __setitem__(self, key, value):
        try:
            old_value = super().__getitem__(key)
        except: old_value = None
        if old_value == None:
            if not isinstance(value, Value):
                value = Value(value)
            super().__setitem__(key, value)
        else:
            if isinstance(value, Value):
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

