#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

class ParserError(Exception):
    """
    Exception to be thrown that the parser is unable to handle.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InvalidIPAddressError(Exception):
    """
    Exception to be thrown when the IP address provided is not a valid IPv4
    address.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CIDRError(Exception):
    """
    Exception to be thrown when the CIDR notation is not valid (i.e. not an
    integer between 1 and 32 inclusive).
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
