import unittest

from structures.records.code import Code
from structures.connector import connect
from structures.records.requirement import Requirement


code = Code("", "global", "asdf", "qwer", "zxvc", [], 1, 3, )
requirement =Requirement('A', 1, 'Test Requirement', 'This is a test requirement.', ['test', 'requirement'])
class TestHarness(unittest.TestCase):
    def test_connect(self):
        connect(requirement, code)
