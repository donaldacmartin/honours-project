class MergedParser(object):
    def __init__(self):
        self.datetime               = None
        self.ip_addr_to_asys        = {}
        self.asys_connections       = set()

    def merge_data(self, bgp_dump1, bgp_dump2):
        merged = bgp_dump1.asys_connections.union(bgp_dump2.asys_connections)
        self.asys_connections = merged

    def merge_lookup(self, bgp_dump1, bgp_dump2)
        
