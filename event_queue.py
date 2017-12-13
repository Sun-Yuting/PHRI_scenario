#!/user/bin/env python
# -*- coding: utf-8 -*-

# TODO multiprocess.Queue
import queue

class EventQueue:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__waiting = queue.Queue()
        self.__accomplished = queue.Queue()
        self.__disposed = queue.Queue()

    def add_event(self, name):
        self.__waiting.put(name)

    def get_event(self):
        if not self.__waiting.empty():
            return self.__waiting.get()

    def check_event(self):
        if self.__waiting.empty():
            return False
        else:
            return True

    def has_event(self, event):
        # Queue can't be iterated
        if event in self.__waiting.queue:
            return True
        else:
            return False

    def add_accomplished(self, name):
        self.__accomplished.put(name)

    def add_disposed(self, name):
        self.__disposed.put(name)