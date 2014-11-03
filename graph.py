#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

import sys
sys.path.append("/home/1101795m/local/lib/python/")

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

from networkx import Graph, ego_graph, graphviz_layout, draw

class NetworkGraph():
    def __init__(self, as_links):
        self.graph = Graph()
        self.__add_edges(as_links)
        self.__draw()
    
    def __add_edges(self, as_links):
        for link in as_links:
            self.graph.add_edge(link[0], link[1])
            
    def __draw(self):
        pos = graphviz_layout(self.graph, prog="twopi", root=0)
        draw(self.graph,
            pos,
            node_color=[self.graph.rtt[v] for v in self.graph],
            with_labels=False,
            alpha=0.5,
            node_size=5)
        plt.savefig('graph_viz_graph.png')