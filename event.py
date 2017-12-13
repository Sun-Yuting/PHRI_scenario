#!/user/bin/env python
# -*- coding: utf-8 -*-


class Event:
    """event class, singleton"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.state = 'accomplished'
        self.name = 'none'
        self.past_events = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_state(self):
        return self.state

    def set_state(self, state):
        if state not in ['waiting', 'undertaking', 'accomplished', 'disposed']:
            raise ValueError('not a legal state!')
        self.state = state

    def add_record(self, name, state):
        self.past_events.append([name, state])
