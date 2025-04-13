#!/usr/bin/env python3

import functools
import logging
import queue
import threading
import urwim.app

class AsyncCaller:
    '''Singleton class which executes function calls in separate thread'''
    class _Caller:
        class Thread(threading.Thread):
            def __init__(self, queue, error_handler):
                self.queue = queue
                self.error_handler = error_handler
                self.logger = logging.getLogger('AsyncCaller')
                super().__init__(daemon=True)

            def run(self):
                while True:
                    async_job = self.queue.get()
                    if async_job == None: break
                    try:
                        async_job()
                        urwim.redraw()
                    except Exception as e:
                        self.error_handler(str(e))

        def __init__(self, error_handler):
            self.queue = queue.Queue()
            self.thread = self.Thread(self.queue, error_handler)
            self.thread.start()

        def call(self, target):
            self.queue.put(target)

    _instance = None

    def __new__(a, error_handler=None):
        if AsyncCaller._instance is None:
            AsyncCaller._instance = AsyncCaller._Caller(error_handler)
        return AsyncCaller._instance


def asynchronous(f):
    '''Decorator which allows any function to be called asynchronously'''
    @functools.wraps(f)
    def _async_call(*args, **kwargs):
        AsyncCaller().call(lambda: f(*args, **kwargs))
    return _async_call

