#!/user/bin/env python
# -*- coding: utf-8 -*-

import threading
import wx

class GUI(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.network = None
        self.stat = None
        self.events =None

    def set_env(self, network, stat, events):
        self.network = network
        self.stat = stat
        self.events = events

    def run(self):
        pass