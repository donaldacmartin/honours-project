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
        super(MergedParser, self).__init__("UPDATES")

        self._merge_date_stamps(parser1, parser2)
        self._merge_asys_connections(parser1, parser2)
        self._merge_asys_ip_addresses(parser1, parser2)

        self.asys_ip_address = parser2.asys_ip_address
        self.asys_size       = parser2.asys_size
        self.visible_blocks  = parser2.visible_blocks

    def _merge_date_stamps(self, parser1, parser2):
        datetime1 = parser1.date_time_stamp
        datetime2 = parser2.date_time_stamp
        self.date_time_stamp = max(datetime1, datetime2)

    def _merge_asys_connections(self, parser1, parser2):
        cxns1 = parser1.asys_connections
        cxns2 = parser2.asys_connections
        self.asys_connections = cxns1.union(cxns2)
