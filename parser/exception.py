class ParserError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InvalidIPAddressError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CIDRError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
