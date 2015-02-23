#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from exception import *
from parser import Parser
from commands import getoutput
from re import sub, compile
from ip_utils import parse_ipv4_block

"""
CiscoParser

An object that takes the file path to a compressed Cisco dump file (with the
.dat.bz2 extension) and converts the contents into data structures defined in
the parent Parser object.

In order to preserve data consistency, this object will block until the file has
been completely parsed.
"""

class CiscoParser(Parser):
    def __init__(self, file_path):
        super(CiscoParser, self).__init__(file_path)

        for line in self.get_lines_from_bzip2(file_path):
            try:
                self.parse_line(line)
            except InvalidIPAddressError as e:
                print("Non-fatal IP address error encountered: " + str(e))
            except CIDRError as e:
                print("Non-fatal CIDR notation error encountered: " + str(e))
            except Exception as e:
                raise ParserError(e.value))

        self.integrity_check()

    def get_lines_from_bzip2(self, file_path):
        stdout = getoutput("bzip2 -d -c " + file_path)
        return stdout.split("\n")

    def parse_line(self, line):
        if not line.startswith("*"):
            return

        tokens    = self.tokenise(line)
        asys_path = self.get_asys_path(tokens)

        if self.contains_two_ip_addrs(tokens):
            ip_addr, cidr_size = parse_ipv4_block(tokens[0])
        else:
            ip_addr, cidr_size = self.previous_alloc

        self.record_line_details(ip_addr, cidr_size, asys_path)
        self.previous_alloc = (ip_addr, cidr_size)

    def tokenise(self, line):
        line   = sub("[*>d]", "", line)
        tokens = line.split(" ")
        return [token for token in tokens if token != ""]

    def get_asys_path(self, tokens):
        path_weight = tokens.index("0")
        asys_path   = tokens[path_weight + 1:]
        return [int(asys) for asys in asys_path if asys.isdigit()]

    def contains_two_ip_addrs(self, tokens):
        ip_addr_regex = compile("\d+\.\d+\.\d+\.\d+")
        return True if ip_addr_regex.match(tokens[1]) is not None else False
