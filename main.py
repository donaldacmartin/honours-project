#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from file import get_file_contents

f = get_file_contents("bgpdata/2001.10/RIBS/rib.20011031.2234.bz2")
print(f)

while True:
    num = input("Please enter a number: ")
    
    if num in f:
        print(f[num])
    else:
        print(str(num) + " is not in index")