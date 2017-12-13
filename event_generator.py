#!/user/bin/env python
# -*- coding: utf-8 -*-

import threading


class EventGenerator(threading.Thread):
    """generate events from parameters"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.network = None
        self.stat = None
        self.events = None
        self.sensing_params = []  # list of strings, see sensing part protocol
        self.tts_params = ''  # "start" or "end"
        self.bm_params = ''  # "start" or "end"

    # override set attribute operator to trigger events when attribute value changes
    def __setattr__(self, key, value):
            # generate events
        if key == 'tts_params' and hasattr(self, 'tts_params'):
            if self.tts_params != value:
                self.events.add_event(f'robot_utter_{value}')
        elif key == 'bm_params' and hasattr(self, 'bm_params'):
            if self.bm_params != value:
                self.events.add_event(f'robot_motion_{value}')
        elif key == 'sensing_params' and hasattr(self, 'sensing_params') and len(self.sensing_params) >= 2:
            # [0]
            if self.sensing_params[0] != value[0]:
                try:
                    audio_params = value[0].split(b',')
                    if len(audio_params) >= 10:
                        vad = int(audio_params[4])
                        self.events.add_event('user_utter_start' if vad == 1 else 'user_utter_end')
                    else:
                        print(audio_params)
                except ValueError:
                    print('svtools value error')
            # [9]
            if self.sensing_params[1] != value[1]:
                self.events.add_event(f'user_head_{value[1][2:-1].lower()}')
        # call super
        super(EventGenerator, self).__setattr__(key, value)

    def set_env(self, network, stat, events):
        self.network = network
        self.stat = stat
        self.events = events

    def run(self):

        while True:
            # for details, see sensing part protocol
            parameters = self.network.recv('sensing').split(' ')
            #print(parameters)
            # [0]
            audio_params = parameters[0].split(',')
            if len(audio_params) >= 10:
                vad = int(audio_params[4])
                if not vad == 0 and not vad == 1:
                    vad = 'pass'
                parameters[0] = vad
            # [9]
            parameters[1] = parameters[1][2:-1].lower()
            print(parameters)
            #self.sensing_params = self.network.recv('sensing').split(' ')
            # (robot_utter) start: 'start', end: 'end'
            #self.tts_params = self.network.recv('tts')
            # (robot_motion) start: 'start', end: 'end'
            #self.bm_params = self.network.recv('bm')
