class ParserException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class IPv4SpaceOverflowException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InvalidIPAddressException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CIDRException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
