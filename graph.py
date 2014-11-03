#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

sys.path.append("/home/1101795m/local/lib/python/")

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

from networkx import Graph, ego_graph, spring_layout, draw, draw_networkx_nodes

class NetworkGraph():
    def __init__(self, as_links):
        self.graph = Graph()
        self.__add_edges(as_links)
        self.__draw()
    
    def __add_edges(self, as_links):
        for link in as_links:
            self.graph.add_edge(link[0], link[1])
            
    def __draw(self):
        nodes = self.graph.Degree()
        (centre, degree) = sorted(nodes.items(), key=itemgetter(1))[-1]
        hub_ego = ego_graph(self.graph, centre)
        pos = spring_layout(hub_ego)
        draw(hub_ego,pos,node_color='b',node_size=50,with_labels=False)
        draw_networkx_nodes(hub_ego,pos,nodelist=[centre],node_size=300,node_color='r')
        plt.savefig('ego_graph.png')