#!/user/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import random
import math


class Executor(threading.Thread):
    """executor class for execution"""

    def __init__(self, r_root, s_root, m_root):
        threading.Thread.__init__(self)
        self.r_root = r_root
        self.s_root = s_root
        self.m_root = m_root
        self.events = None
        self.network = None
        self.stat = None

        self.time_base = 0

    def set_env(self, network, stat, events):
        self.events = events
        self.stat = stat
        self.network = network

    @staticmethod
    def check_chance(chance):
        if chance >= random.random():
            return True
        return False

    @staticmethod
    def get_time(para):
        dist = para.get('distribution')
        if dist == 'uniform':
            minim = float(para.get('min'))
            maxim = float(para.get('max'))
            return random.uniform(minim, maxim)
        elif dist == 'normal':
            average = float(para.get('average'))
            standard = math.sqrt(float(para.get('variance')))
            return random.gauss(average, standard)

    def apply_rules(self, event):
        rules = []
        for rule in self.r_root:
            if rule.get('trigger') == event:
                if self.check_chance(float(rule.get('chance'))):
                    rules.append(rule)

        if len(rules) == 0:
            return None

        return rules

    def apply_metas(self, rules):
        if rules is None:
            return None

        rule_list = ' '.join([rule.get('name') for rule in rules])

        for meta in self.m_root:
            if meta.get('trigger') in rule_list:
                if self.check_chance(float(meta.get('chance'))):
                    return self.apply_rules(meta.text)[0]

        # if no meta rules matches, return the first rule matched
        return rules[0]

    def check_timeout(self, timeout):
        if self.time_base == 0:
            self.time_base = time.time()
            return False
        else:
            if float(timeout) <= time.time() - self.time_base:
                self.time_base = 0
                return True
            else:
                return False

    def check_condition(self, condition):
        # types:
        # rightNow
        # waitEvent event_name [timeout]
        # waitTime time
        # checkState user_state wait|skip
        tokens = condition.split(' ')
        if tokens[0] == 'rightNow':
            return True
        elif tokens[0] == 'waitEvent':
            if len(tokens) == 3:
                if self.check_timeout(tokens[2]):
                    return 'skip'
            # wait for event while rule matching still running
            # not strictly logical
            if self.events.has_event(tokens[1]):
                return True
            else:
                return False
        elif tokens[0] == 'waitTime':
            if self.check_timeout(tokens[1]):
                return True
            else:
                return False
        elif tokens[0] == 'checkState':
            if self.stat.check_state(tokens[1]):
                return True
            elif tokens[2] == 'wait':
                return False
            elif tokens[2] == 'skip':
                return 'skip'

    def execute(self, tag, rule_type):
        # command format motion: "name target delay duration"
        # command format utter: "SPEAK content delay"

        if rule_type == 'motion':

            name = tag.text.strip()  # str.strip(), remove leading and ending spaces
            target = ''
            delay = ''
            duration = ''

            for para in list(tag):
                if para.get('name') == 'target':
                    target = para.get('target')
                elif para.get('name') == 'delay':
                    if para.get('time', False):
                        delay = para.get('time')
                    elif para.get('distribution', False):
                        delay = self.get_time(para)
                    else:
                        raise SyntaxError('syntax error in rule.xml')
                elif para.get('name') == 'duration':
                    if para.get('time', False):
                        duration = para.get('time')
                    elif para.get('distribution', False):
                        duration = self.get_time(para)
                    else:
                        raise SyntaxError('syntax error in rule.xml')
            print(f'name:{name} target:{target} delay:{delay} duration:{duration}')
            #self.network.send(f'{name} {target} {delay} {duration}', 'bm')

        if rule_type == 'utter':

            content = ''
            delay = ''

            for para in list(tag):
                if para.get('name') == 'content':
                    content = para.get('content')
                elif para.get('name') == 'delay':
                    if para.get('time', False):
                        delay = para.get('time')
                    elif para.get('distribution', False):
                        delay = self.get_time(para)
                    else:
                        raise SyntaxError('syntax error in rule.xml')

            print(f'name:SPEAK content:{content} delay:{delay}')
            #self.network.send(f'SPEAK {content} {delay}', 'tts')

        return True

    def run(self):
        while True:
            # .. rule parts
            if self.events.check_event():
                event = self.events.get_event()
                rules = self.apply_rules(event)
                definitive_rule = self.apply_metas(rules)
                if definitive_rule is None:
                    self.events.add_disposed(event)
                else:
                    self.execute(definitive_rule, definitive_rule.get('type'))
                    self.events.add_accomplished(event)
                continue

            # .. scenario part
            lines = list(self.s_root)
            #print(lines[0].get('id'))
            if len(lines) == 0:
                continue
            result = self.check_condition(lines[0].get('condition'))
            if result:
                self.execute(lines[0], lines[0].get('type'))
                del self.s_root[0]
            elif result == 'skip':
                del self.s_root[0]
