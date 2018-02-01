#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
Proximate Human-Robot Interaction System -- Scenario Part

@Last Update: 2017.12.21

@Author: Sun Yuting
@Email: sunyuting798@gmail.com | sunyuting798@126.com
"""

import xml_parser
import executor
import event_generator
import sys
import net
import event_queue
import state


# TODO: xml checker
def check_xml(root):
    """
    Checks the syntax of an xml file.

    :param root: root of the parsed xml file
    :return: True or False on whether check passed
    """
    return True


def main(rule_file="rule.xml", scenario_file="scenario.xml", meta_file="meta_rule.xml"):
    # parse
    parser = xml_parser.XmlParser(rule_file, scenario_file, meta_file)
    _, r_root, _, s_root, _, m_root = parser.get_result()
    print('info: xml files parsed')

    # check syntax of xml files
    if not check_xml(r_root):
        raise SyntaxError(f'syntax error found in {rule_file}!')
    if not check_xml(s_root):
        raise SyntaxError(f'syntax error found in {scenario_file}!')
    if not check_xml(m_root):
        raise SyntaxError(f'syntax error found in {meta_file}!')
    print('info: syntax check passed')

    # get ready for net, state, event queue
    # making these singleton is better
    network = net.Net()
    stat = state.State()
    events = event_queue.EventQueue()
    print('info: environment initialed')

    # thread for executor
    ex_thread = executor.Executor(r_root, s_root, m_root)
    ex_thread.set_env(network, stat, events)
    ex_thread.start()
    print('info: executor started.')

    # thread for event generator
    eg_thread = event_generator.EventGenerator()
    eg_thread.set_env(network, stat, events)
    eg_thread.start()
    print('info: event generator started.')

    ex_thread.join()
    eg_thread.join()


if __name__ == '__main__':
    main()
