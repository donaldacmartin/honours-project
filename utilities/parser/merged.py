#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from parser import Parser

"""
MergedParser

An object to reconcile multiple router dumps. This object can accept both Cisco
and BGP router dump parsers and merge them.

Note: as the Internet is expanding in size, the visible address space is not
being recalculated, but rather the larger of the two values is being used. This
is the same for the number of allocated blocks in CIDR notation.
"""

class MergedParser(Parser):
    def __init__(self, parser1, parser2):
        super(MergedParser, self).__init__()

        self._merge_as_connections(parser1, parser2)
        self._merge_as_to_ip_addresses(parser1, parser2)
        self._merge_alloc_sizes(parser1, parser2)
        self._merge_alloc_blocks(parser1, parser2)
        self._merge_visible_address_space(parser1, parser2)

    def _merge_as_connections(self, parser1, parser2):
        connections1        = parser1.as_connections
        connections2        = parser2.as_connections
        self.as_connections = connections1.union(connections2)

    def _merge_as_to_ip_addresses(self, parser1, parser2):
        ips1                  = parser1.as_to_ip_address
        ips2                  = parser2.as_to_ip_address
        self.as_to_ip_address = dict(list(ips1.items()) + list(ips2.items()))

    def _merge_alloc_sizes(self, parser1, parser2):
        allocs1            = parser1.as_alloc_size
        allocs2            = parser2.as_alloc_size
        self.as_alloc_size = dict(list(allocs1.items()) + list(allocs2.items()))

    def _merge_alloc_blocks(self, parser1, parser2):
        for i in range(32):
            allocs1 = parser1.alloc_blocks
            allocs2 = parser2.alloc_blocks
            self.alloc_blocks[i] = max(allocs1, allocs2)

    def _merge_visible_address_space(self, parser1, parser2):
        space1                     = parser1.visible_address_space
        space2                     = parser2.visible_address_space
        self.visible_address_space = max(space1, space2)
