from unittest import TestCase

class TestASLookup(TestCase):
    def setUp(self):
        self.as_lookup = ASLookup()

    def test_as_num(self):
        self.assertTrue(1 in self.as_lookup)

    def test_invalid_as_num(self):
        self.assertTrue(-1 not in self.as_lookup)
