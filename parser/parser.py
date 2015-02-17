#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from utilities.file.name import get_date_for_filename
from ip_utils import ip_to_int, int_to_ip, cidr_to_int

class Parser(object):
    def __init__(self, filename):
        self.datetime               = get_date_for_filename(filename)
        self.asys_to_ip_addr        = {}
        self.ip_addr_to_asys        = {}
        self.asys_connections       = set()
        self.asys_size              = {}
        self.visible_blocks         = []
        self.ip_block_path          = {}
        self.highest_ip_encountered = 0

    # --------------------------------------------------------------------------
    # Public Functions
    # --------------------------------------------------------------------------

    def get_visible_space_size(self):
        block_sizes = [cidr_to_int(cidr) for (_, cidr) in self.visible_blocks]
        return sum(block_sizes)

    def get_block_size_totals(self):
        totals = [0] * 32

        for (ip, cidr) in self.visible_blocks:
            totals[cidr - 1] += 1

        return totals

    def get_multicast_ip_addrs(self):
        multicasts = []

        for (ip_addr, asys_group) in self.ip_addr_to_asys.values():
            if len(asys_group) > 1:
                multicasts.append(ip_addr)

        return [int_to_ip(ip_addr) for ip_addr in multicasts]

    # --------------------------------------------------------------------------
    # Recording data from derived parsers
    # --------------------------------------------------------------------------

    def record_line_details(self, ip_addr, cidr_size, asys_path):
        self.record_asys_connections(asys_path)

        if not self.ip_addr_already_recorded(ip_addr):
            self.record_ip_addr_asys(ip_addr, asys_path)
            self.record_asys_size(asys_path, cidr_size)
            self.mark_block_visible(ip_addr, cidr_size)
            self.record_asys_path(ip_addr, cidr_size)

    def record_asys_connections(self, asys_path):
        for counter in range(1, len(asys_path)):
            prev_asys  = asys_path[counter - 1]
            curr_asys  = asys_path[counter]
            connection = (min(prev_asys, curr_asys), max(prev_asys, curr_asys))
            self.asys_connections.add(connection)

    def ip_addr_already_recorded(self, ip_addr):
        ip_as_int = ip_to_int(ip_addr)
        return ip_as_int <= self.highest_ip_encountered

    def record_ip_addr_asys(self, ip_addr, asys_path):
        ip_as_int = ip_to_int(ip_addr)
        dest_asys = asys_path[-1]

        if dest_asys not in self.asys_to_ip_addr:
            self.asys_to_ip_addr[dest_asys] = set()

        if ip_as_int not in self.ip_addr_to_asys:
            self.ip_addr_to_asys[ip_as_int] = set()

        self.asys_to_ip_addr[dest_asys].add(ip_as_int)
        self.ip_addr_to_asys[ip_as_int].add(dest_asys)

    def record_asys_size(self, asys_path, cidr_size):
        asys = asys_path[-1]
        size = cidr_to_int(cidr_size)
        self.asys_size[asys] += size if asys in self.asys_size else size

    def record_asys_path(self, ip_addr, asys_path):
        ip_as_int = ip_to_int(ip_addr)

        if ip_as_int not in self.ip_block_path:
            self.ip_block_path[ip_as_int] = set()

        self.ip_block_path[ip_as_int].add(asys_path)

    def mark_block_visible(self, ip_addr, cidr_size):
        ip_as_int = ip_to_int(ip_addr)
        ip_block  = (ip_as_int, prefix_size)
        size      = cidr_to_int(cidr_size)

        self.visible_blocks.append(ip_block)
        self.highest_ip_encountered = ip_as_int + size
