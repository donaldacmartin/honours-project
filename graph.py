#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

from networkx import Graph, ego_graph, graphviz_layout, draw

class NetworkGraph():
    def __init__(self, file_name):
        self.graph = Graph()
        self.file = file_name
    
    def add_edges(self, as_links):        
        for link in as_links:
            self.graph.add_edge(link[0], link[1])
            self.size -= 1
            
            if self.size < 0:
                break
            
    def draw(self):
        plt.figure(figsize=(50,50))
        draw(self.graph, node_size=10)
        plt.savefig(self.file)