from unittest import TestCase, main
from utilities.as_lookup import ASLookup

class TestASLookup(TestCase):
    def setUp(self):
        self.as_lookup = ASLookup().table

    def test_as_num(self):
        self.assertTrue(1 in self.as_lookup)

    def test_invalid_as_num(self):
        self.assertTrue(-1 not in self.as_lookup)

if __name__ == "__main__":
    main()
