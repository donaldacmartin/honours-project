#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from file import *
from threading import Thread

def master_method():
    files = FileFinder("/nas05/users/csp/routing-data/").get_files()
    
    for f in files:
        print(f.get_name(), f.get_date())

thread_master = threading.Thread(target=master_method)