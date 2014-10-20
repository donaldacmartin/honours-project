#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

class AutonomousSystem():
    def __init__(self):
        self.index = 0
        self.name = ""
        self.peers = []
        
    def set_index(self, index):
        self.index = index
    
    def set_name(self, name):
        self.name = name
        
    def add_peer(self, peer):
        self.peers.append(peer)
    
    def __str__(self):
        return "Name: " + self.name + "\nIndex: AS" + str(self.index) + "\n"