#!/usr/bin/python
#
# Donald Martin
# Honours Project: Map of the Internet (2014/15)
# University of Glasgow

from graphs.graph import LIGHT_GREY, DARK_RED

class HiddenRoutesAtlas(AtlasMap):
    def __init__(self, width, height, bgp_dumps, region=GLOBAL):
        if len(bgp_dumps) < 1 or bgp_dumps is None:
            return

        super(HiddenRoutesAtlas, self).__init__(width, height, bgp_dumps[0], region, LIGHT_GREY)
        all_possible_routes = self._get_all_routes(bgp_dumps)
        routes_avail_to_all = self._get_routes_available_to_all_routers(bgp_dumps)

        self._draw_routes(all_possible_routes, LIGHT_GREY)
        self._draw_routes(routes_avail_to_all, DARK_RED)

    def _get_all_routes(self, bgp_dumps):
        all_routes = bgp_dumps[0].asys_connections

        for bgp_dump in bgp_dumps:
            all_routes = all_routes.union(bgp_dump.asys_connections)

        return all_routes

    def _get_routes_available_to_all_routers(self, bgp_dumps):
        routes = bgp_dumps[0].asys_connections

        for bgp_dump in bgp_dumps:
            routes = routes.intersection(bgp_dump.asys_connections)

        return routes

    def _draw_routes(self, routes, colour):
        for (start, end) in routes:
            super(ChronoAtlasMap, self)._draw_line(start, end, colour)
