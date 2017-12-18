#!/user/bin/env python
# -*- coding: utf-8 -*-


class State:

    def __init__(self):
        self.user_silence = True
        self.user_head_state = None

    def check_state(self, state):
        if hasattr(self, state):
            return getattr(self, state)