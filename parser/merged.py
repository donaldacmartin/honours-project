class MergedParser(object):
    def __init__(self, bgp_dump1, bgp_dump2):
        self.merge_connections(bgp_dump1, bgp_dump2)
        self.merge_ip_lookup(bgp_dump1, bgp_dump2)
        self.merge_asys_lookup(bgp_dump1, bgp_dump2)

        self.asys_size      = bgp_dump1.asys_size
        self.visible_blocks = bgp_dump1.visible_blocks
        self.ip_block_path  = bgp_dump1.ip_block_path

    def merge_connections(self, bgp_dump1, bgp_dump2):
        merged = bgp_dump1.asys_connections.union(bgp_dump2.asys_connections)
        self.asys_connections = merged

    def merge_ip_lookup(self, bgp_dump1, bgp_dump2):
        self.asys_to_ip_addr = bgp_dump1.asys_to_ip_addr
        self.asys_to_ip_addr.update(bgp_dump2.asys_to_ip_addr)

    def merge_asys_lookup(self, bgp_dump1, bgp_dump2):
        self.ip_addr_to_asys = bgp_dump1.ip_addr_to_asys
        self.ip_addr_to_asys.update(bgp_dump2.ip_addr_to_asys)
