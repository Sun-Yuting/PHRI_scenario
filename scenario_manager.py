#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
Proximate Human-Robot Interaction System -- Scenario Part

@Last Update: 2017.12.13

@Author: Sun Yuting
@Email: sunyuting798@gmail.com | sunyuting798@126.com

@Dependency:
[0] python, version 3.6 or higher
[1] xml files: rule file, meta rule file & scenario file
[2] PHRI sensing part
[3] tts engine, robot motion server
"""

import xml_parser
import executor
import event_generator
import gui
import sys
import net
import event_queue
import state


def check_xml(root):
    return True


def main(rule_file="rule.xml", scenario_file="scenario.xml", meta_file="meta_rule.xml"):
    # parse
    parser = xml_parser.XmlParser(rule_file, scenario_file, meta_file)
    _, r_root, _, s_root, _, m_root = parser.get_result()
    print('xml files parsed')

    # TODO check xml syntax
    if not check_xml(r_root):
        raise SyntaxError(f'syntax error found in {rule_file}!')
    if not check_xml(s_root):
        raise SyntaxError(f'syntax error found in {scenario_file}!')
    if not check_xml(m_root):
        raise SyntaxError(f'syntax error found in {meta_file}!')
    print('syntax check passed')

    # get ready for net, state, event queue
    network = net.Net()
    stat = state.State()
    events = event_queue.EventQueue()

    # thread for executor
    ex_thread = executor.Executor(r_root, s_root, m_root)
    ex_thread.set_env(network, stat, events)
    ex_thread.start()
    print('executor started.')

    # thread for event generator
    eg_thread = event_generator.EventGenerator()
    eg_thread.set_env(network, stat, events)
    eg_thread.start()
    print('event generator started.')

    # thread for user interface
    gui_thread = gui.GUI()
    gui_thread.set_env(network, stat, events)
    gui_thread.start()
    print('GUI launched.')

    ex_thread.join()
    eg_thread.join()
    gui_thread.join()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
