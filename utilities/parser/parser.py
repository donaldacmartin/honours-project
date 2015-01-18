#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from commands import getoutput
from utilities.file.name import get_date_for_filename
from ip_utils import ip_to_int, cidr_to_int

"""
Parser

A generic object to provide data structures that all specialised parsers should
fill and some generic functions for converting between human readable numbers
and network formats (eg CIDR notation).

This object is the equivelant of a Java abstract class, and should not be
instantiated directly: use one of the two subclasses BGPParser or CiscoParser.
"""

class Parser(object):
    def __init__(self, filename):
        self.date_time_stamp  = get_date_for_filename(filename)
        self.as_connections   = set()
        self.as_to_ip_address = {}
        self.as_alloc_size    = {}
        self.visible_blocks   = []

    # --------------------------------------------------------------------------
    # Higher Order Functions
    # --------------------------------------------------------------------------

    def _convert_cmd_to_lines(self, cmd):
        stdout = getoutput(cmd)
        return stdout.split("\n")

    def _add_asys_path(self, asys_path):
        for i in range(1, len(asys_path)):
            prev = asys_path[i-1]
            curr = asys_path[i]
            self._add_asys_connection(prev, curr)

    def _record_information(self, ip_address, prefix_size, asys):
        self._record_asys_ip(asys, ip_address)

        if not self._ip_already_visited(ip_addr, prefix_size):
            self._mark_alloc_block_visible(ip_address, prefix_size)
            self._record_asys_size(asys, prefix_size)

    # --------------------------------------------------------------------------
    # Data Structure Manipulation
    # --------------------------------------------------------------------------

    def _add_asys_connection(self, asys1, asys2):
        connection = (min(asys1, asys2), max(asys1, asys2))
        self.as_connections.add(connection)

    def _mark_alloc_block_visible(self, ip_address, prefix_size):
        ip_block = (ip_to_int(ip_address), prefix_size)
        self.visible_blocks.append(ip_block)
        self.visible_blocks = sorted(self.visible_blocks)

    def _record_asys_ip(self, asys, ip_address):
        if asys not in self.asys_ip_address:
            self.asys_ip_address[asys] = set()

        self.asys_ip_address[asys].add(ip_address)

    def _record_asys_size(self, asys, prefix_size):
        if asys not in self.asys_size:
            self.asys_size[asys] = 0

        self.asys_size[asys] += cidr_to_int(prefix_size)

    def _ip_already_visited(self, ip_address, prefix_size):
        ip_int = ip_to_int(ip_address)
        entry  = (ip_int, prefix_size)
        prev_ip_index = bisect_left(self.visible_blocks, entry) - 1

        if prev_ip_index < 0:
            return False

        prev_ip_block = self.visible_blocks[prev_ip_index]
        prev_ip       = prev_ip_block[0]
        prev_size     = cidr_to_int(prev_ip_block[1])

        return prev_ip <= ip_int <= (prev_ip + prev_size)
