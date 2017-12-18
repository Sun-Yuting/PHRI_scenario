#!/user/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os.path


class XmlParser:
    """xml files parser"""

    def __init__(self, rule_file="rule.xml", scenario_file="scenario.xml", meta_file="meta_rule.xml"):
        if not os.path.isfile(rule_file) or not os.path.isfile(scenario_file) or not os.path.isfile(meta_file):
            raise ValueError("no xml files!")
        self.rule_file = rule_file
        self.scenario_file = scenario_file
        self.meta_file = meta_file
        self.r_tree, self.r_root = self.parse(rule_file)
        self.s_tree, self.s_root = self.parse(scenario_file)
        self.m_tree, self.m_root = self.parse(meta_file)

    @staticmethod
    def parse(addr):
        tree = ET.parse(addr)
        root = tree.getroot()

        return tree, root

    def get_result(self):
        return self.r_tree, self.r_root, self.s_tree, self.s_root, self.m_tree, self.m_root

    def get_rule_file(self):
        return self.rule_file

    def set_rule_file(self, rule_file, reparse=False):
        self.rule_file = rule_file
        if reparse:
            self.r_tree, self.r_root = self.parse(rule_file)

    def get_scenario_file(self):
        return self.scenario_file

    def set_scenario_file(self, scenario_file, reparse=False):
        self.scenario_file = scenario_file
        if reparse:
            self.s_tree, self.s_root = self.parse(scenario_file)
