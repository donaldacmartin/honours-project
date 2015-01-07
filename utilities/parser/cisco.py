#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from parser import Parser
from re import sub, compile

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
        super(CiscoParser, self).__init__()
        lines = self._convert_cmd_to_lines("bzip2 -d -c " + file_path)

        for line in lines:
            self._parse_line(line)

    def _parse_line(self, line):
        if not line.startswith("*"):
            return

        tokens              = self._tokenise(line)
        ip_addr, alloc_size = self._get_allocated_base_ip_and_size(tokens)
        asys                = self._add_asys_path_and_get_dest_asys(tokens)

        if ip_addr is not None:
            self._record_ip_alloc_size(ip_addr, alloc_size, asys)

    def _tokenise(self, line):
        line   = sub("[*>d]", "", line)
        tokens = line.split(" ")
        return [token for token in tokens if token != ""]

    def _get_allocated_base_ip_and_size(self, tokens):
        if not self._contains_two_ip_addrs(tokens):
            return (None, None)

        return self._convert_ip_block_to_base_and_size(tokens[0])

    def _add_asys_path_and_get_dest_asys(self, tokens):
        path_weight = tokens.index("0")
        asys_path   = tokens[path_weight + 1:]
        asys_path   = [int(asys) for asys in asys_path if asys.isdigit()]

        self._add_asys_path(asys_path)
        return asys_path[-1]

    def _contains_two_ip_addrs(self, tokens):
        ip_addr_regex = compile("\d+\.\d+\.\d+\.\d+")
        return True if ip_addr_regex.match(tokens[1]) is not None else False
