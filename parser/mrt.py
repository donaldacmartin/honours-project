#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from parser import Parser
from commands import getoutput
from ip_utils import parse_ipv4_block

class MRTParser(Parser):
    def __init__(self, file_path):
        super(MRTParser, self).__init__(file_path)
        lines = get_lines_from_bgpdump(file_path)

        for line in lines:
            self._parse_line(line)

    def get_lines_from_bgpdump(file_path):
        stdout = getoutput("bgpdump -m " + file_path)
        return stdout.split("\n")

    def parse_line(self, line):
        if line == "" or line == " " or "[info] logging to syslog" in line:
            return

        tokens = line.split("|")

        try:
            ip_address, cidr_size = parse_ipv4_block(tokens[5])
            asys_path             = self.get_asys_path(tokens)
            self.record_line_details(ip_addr, cidr_size, asys_path)
        except Exception as e:
            print("Line: " + line)

    def get_asys_path(self, tokens):
        hops = tokens[6].split(" ")
        return [int(asys) for asys in hops if asys.isdigit()]
