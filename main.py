#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from subprocess import check_output, STDOUT

def is_bgpdump_installed():
    try:
        output = check_output("bgpdump", shell=True, stderr=STDOUT)
    except Exception, e:
        output = str(e.output)
    
    return "bgpdump version" in output

def convert_bgp_data_to_ascii():
    pass
    
def read_ascii_into_python():
    pass
    
if is_bgpdump_installed():
    print("BGPDump is installed")
else:
    print("BGPDump is not installed")