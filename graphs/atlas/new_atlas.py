from base_atlas import BaseAtlas

class StandardAtlas(BaseAtlas):
    def __init__(self, bgp_dump, width, height, region):
        super(StandardAtlas).__init__(width, height, region)

        self.resolve_bgp_to_asys_coords(bgp_dump)
        self.draw_connections(bgp_dump.asys_connections)
