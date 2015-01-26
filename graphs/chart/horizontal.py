#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from graphs.graph import Graph, DARK_RED
from utilities.parser.ip_utils import cidr_to_int, ip_to_int

class HorizontalChart(Graph):
    def __init__(self, width, height, bgp_dumps):
        super(Horizontal).__init__(width, height)

        base     = ip_to_int("4.0.0.0")
        limit    = ip_to_int("4.255.255.255")
        ip_range = limit / base

        for bgp_dump in bgp_dumps:
            blocks = bgp_dump.visible_blocks
            blocks = [(ip, cidr) for (ip,cidr) in blocks if base <= ip <= limit]

            for (ip, cidr) in blocks:
                start = (ip - base) * ip_range
                end   = ((ip + cidr_to_int(cidr)) - base) * ip_range
                self.draw_line((start, 50), (end, 50))
