#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from parser import Parser

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
        visited_ips = set()

        for line in lines:
            self._parse_line(line, visited_ips)

        self._update_size()

    def _parse_line(self, line, visited_ips):
        if line == "" or line == " " or "[info] logging to syslog" in line:
            return

        tokens              = line.split("|")
        ip_addr, alloc_size = self._convert_ip_block_to_base_and_size(tokens[5])
        asys                = self._add_asys_path_and_get_dest_asys(tokens)

        if ip_addr is not None and ip_addr not in visited_ips:
            self._record_ip_alloc_size(ip_addr, alloc_size, asys)
            visited_ips.add(ip_addr)

    def _add_asys_path_and_get_dest_asys(self, tokens):
        asys_hops = tokens[6].split(" ")
        asys_path = [int(asys) for asys in asys_hops if asys.isdigit()]
        self._add_asys_path(asys_path)
        return asys_path[-1]
