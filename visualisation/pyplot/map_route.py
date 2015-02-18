from sys import path
path.append("lib")

from matplotlib import use
use("agg")
from networkx import draw, DiGraph
from matplotlib.pyplot import savefig
from utilities.as_lookup import ASLookup

def map_route_to_ip(ip_addr, bgp_dump):
    graph     = nx.DiGraph()
    as_lookup = ASLookup()
    paths     = bgp_dump.ip_block_path[ip_addr]

    for path in paths:
        graph.add_edge("Start", as_lookup.get_org_for_asys(path[0]))

        for i in range(1, len(path)):
            previous_hop = path[i - 1]
            this_hop     = path[i]

            previous_hop = as_lookup.get_org_for_asys(previous_hop)
            this_hop     = as_lookup.get_org_for_asys(this_hop)
            graph.add_edge(previous_hop, this_hop)

    draw(graph)
    savefig("trial.png")
