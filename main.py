#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from graphs import RingGraph, StaggeredRingGraph
from atlas_map import AtlasMap
from file import *
from chrono_atlas_map import ChronologicalAtlasMap
import logging

logging.basicConfig(format="%(asctime)s %(message)s", filename="log.out")
