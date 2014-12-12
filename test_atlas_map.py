#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

import unittest
from time import time
from atlas_map import AtlasMap
from file import BGPDumpExecutor
from PIL import Image
from os import remove, path

"""
AtlasMapTest


"""

class AtlasMapTest(unittest.TestCase):
    def setUp(self):
        self.expected_image  = Image.open("test_cases/simple_atlas_map.png")
        self.simple_bgp_file = """/nas05/users/csp/routing-data/
                               archive.routeviews.org/bgpdata/2001.10/RIBS/
                               rib.20011027.0849.bz2"""
        
    def test_image_is_generated(self):
        filename = "test-atlas-map.png"
        
        try:
            remove(filename) if path.exists(filename) else None
            bgp_dump  = BGPDumpExecutor(self.simple_bgp_file)
            atlas_map = setup_atlas_map(bgp_dump)
            atlas_map.save_graph(filename)
        except:
            error_msg = "Unable to generate the image"
            self.assertTrue(False, error_msg)
    
    def test_image_matches(self):
        bgp_dump  = BGPDumpExecutor(self.simple_bgp_file)
        atlas_map = setup_atlas_map(bgp_dump)
        
        generated_image = atlas_map.draw_graph()
        
        error_msg = "Generated picture did not match expected picture"
        self.assertEqual(self.expected_image, generated_image, error_msg)
        
    def test_reasonable_time(self):
        start_time = time()
        
        bgp_dump  = BGPDumpExecutor(self.simple_bgp_file)
        atlas_map = setup_atlas_map(bgp_dump)
        atlas_map.draw_graph()
        
        end_time = time()
        
        error_msg = "Simple graph took longer than 10 minutes to generate"
        self.assertTrue((end_time - start_time) <= 600, error_msg)
        
def setup_atlas_map(bgp_dump):
    atlas_map = AtlasMap(20000, 100000)
        
    for auto_sys in bgp_dump.ip_addresses:
        atlas_map.add_auto_sys_ip(auto_sys, ip_addresses[auto_sys])
        
    for (start, end) in bgp_dump.connections:
        atlas_map.add_link(start, end)
        
    return atlas_map
  
if __name__ == "__main__":
    unittest.main()