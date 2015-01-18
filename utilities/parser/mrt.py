#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from parser import Parser
from ip_utils import parse_ipv4_block

"""
MRTParser

An object that takes the file path to a compressed MRT dump file (with the .bz2
extension) and converts the contents into data structures defined in the parent
Parser object.

In order to preserve data consistency, this object will block until the file has
been completely parsed.
"""

class MRTParser(Parser):
    def __init__(self, file_path):
        super(MRTParser, self).__init__(file_path)
        lines = self._convert_cmd_to_lines("bgpdump -m " + file_path)

        for line in lines:
            self._parse_line(line)

    def _parse_line(self, line):
        if line == "" or line == " " or "[info] logging to syslog" in line:
            return

        tokens = line.split("|")

        try:
            ip_address, prefix_size = parse_ipv4_block(tokens[5])
        except Exception as e:
            print(e)
            return

        asys = self._add_asys_path_and_get_dest_asys(tokens)
        self._record_information(ip_address, prefix_size, asys)

    def _add_asys_path_and_get_dest_asys(self, tokens):
        asys_hops = tokens[6].split(" ")
        asys_path = [int(asys) for asys in asys_hops if asys.isdigit()]
        self._add_asys_path(asys_path)
        return asys_path[-1]
