#!/user/bin/env python
# -*- coding: utf-8 -*-


class State:

    def __init__(self):
        self.user_silence = True

    def check_state(self, state):
        if hasattr(self, state):
            return getattr(self, state)