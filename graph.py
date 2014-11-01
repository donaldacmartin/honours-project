#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from file import get_file_contents

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.readwrite.dot import write

import graphviz as gv

f = get_file_contents("bgpdata/2001.10/RIBS/rib.20011031.2234.bz2")

gr = graph()

gr.add_nodes(f.keys())

for AS in f.keys():
    for link in f[AS]:
        try:
            gr.add_edge((AS, link))
        except:
            print("Tried to add an existing edge")
        
dot = write(gr)
gvv = gv.Graph(dot)
gv.layout(prog="dot")
gv.draw("file.png")