#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from unittest import TestCase
from utilities.parser.cisco import CiscoParser

TEST_DIR = "test/files/"

class CiscoParserTest(TestCase):
    def test_valid_file(self):
        parser = CiscoParser(TESTDIR + "valid.cisco")
        pass

    def test_invalid_file(self):
        parser = CiscoParser(TESTDIR + "invalid.cisco")
        pass

    def test_no_file(self):
        parser = CiscoParser()
        pass
