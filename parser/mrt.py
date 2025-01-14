#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from exception import *
from parser import Parser
from commands import getoutput
from ip_utils import parse_ipv4_block

class MRTParser(Parser):
    """
    Takes an MRT format routing table dump and converts it to the data
    structures defined in the Parser class.
    """
    def __init__(self, file_path=None):
        super(MRTParser, self).__init__(file_path)

        if file_path is None:
            return

        for line in self.get_lines_from_bgpdump(file_path):
            try:
                self.parse_line(line)
            except InvalidIPAddressError as e:
                print("Non-fatal IP address error encountered: " + str(e))
            except CIDRError as e:
                print("Non-fatal CIDR notation error encountered: " + str(e))
            except Exception as e:
                raise ParserError(str(e))

        self.integrity_check()

    def get_lines_from_bgpdump(self, file_path):
        stdout = getoutput("bgpdump -m " + file_path)
        return stdout.split("\n")

    def parse_line(self, line):
        if line == "" or line == " " or "[info] logging to syslog" in line:
            return

        tokens = line.split("|")

        if len(tokens) != 15:
            raise Exception("Invalid number of components in line")

        ip_addr, cidr_size = parse_ipv4_block(tokens[5])
        asys_path          = self.get_asys_path(tokens)
        self.record_line_details(ip_addr, cidr_size, asys_path)

    def get_asys_path(self, tokens):
        hops = tokens[6].split(" ")
        return [int(asys) for asys in hops if asys.isdigit()]
