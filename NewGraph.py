class NewGraph():
    def __init__(self):
        self.nodes = {}
        
    def add_link(self, node1, node2):
        if node1 in self.nodes:
            self.nodes[node1].append(node2)
        else:
            self.nodes[node1] = [node2]