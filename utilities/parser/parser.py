#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from commands import getoutput
from math import log

"""
Parser

A generic object to provide data structures that all specialised parsers should
fill and some generic functions for converting between human readable numbers
and network formats (eg CIDR notation).

This object is the equivelant of a Java abstract class, and should not be
instantiated directly: use one of the two subclasses BGPParser or CiscoParser.
"""

class Parser(object):
    def __init__(self):
        self.as_connections        = set()
        self.as_to_ip_address      = {}
        self.as_alloc_size         = {}
        self.alloc_blocks          = [0 for _ in range(32)]
        self.visible_address_space = 0

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

    def _convert_ip_block_to_base_and_size(self, ip_block):
        if "/" in ip_block:
            ip_addr, cidr = ip_block.split("/")
            alloc_size    = self._convert_cidr_to_size(cidr)
        else:
            ip_addr       = ip_block
            alloc_size    = self._convert_sig_figs_to_size(ip_block)

        return ip_addr, alloc_size

    # --------------------------------------------------------------------------
    # Data Structure Manipulation
    # --------------------------------------------------------------------------

    def _add_asys_connection(self, asys1, asys2):
        connection = (min(asys1, asys2), max(asys1, asys2))
        self.as_connections.add(connection)

    def _record_ip_alloc_size(self, ip_addr, alloc_size, asys):
        self.as_to_ip_address[asys] = ip_addr

        if asys not in self.as_alloc_size:
            self.as_alloc_size[asys] = 0

        self.as_alloc_size[asys] += alloc_size
        cidr_block = self._convert_size_to_cidr(alloc_size)
        self.alloc_blocks[cidr_block] += 1

        self.visible_address_space += alloc_size

    # --------------------------------------------------------------------------
    # Network Notation Conversions
    # --------------------------------------------------------------------------

    def _convert_cidr_to_size(self, cidr):
        cidr = int(cidr)
        host = 32 - cidr
        return 2 ** host

    def _convert_size_to_cidr(self, size):
        bits = int(log(alloc_size, 2))
        return bits + 32

    def _convert_sig_figs_to_size(self, ip_addr):
        ip_addr = [int(bits) for bits in ip_addr.split(".")]

        for i in range(3, -1, -1):
            if ip_addr[i] > 0:
                break

        return 255 ** (3 - i)
