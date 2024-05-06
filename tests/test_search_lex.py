import unittest

from lexical.search import interpret
from structures import requirement_list
from structures.code import Code
from structures.requirement import Requirement


class TestHarness(unittest.TestCase):
    def setUp(self):
        req1 = Requirement("", "", "", "", ["test1", "test2"])
        req2 = Requirement("", "", "", "", ["test2"])
        req3 = Requirement("", "", "", "", ["test1"])
        req4 = Requirement("", "", "", "", [])
        requirement_list.append(req1)
        requirement_list.append(req2)
        requirement_list.append(req3)
        requirement_list.append(req4)

    def tearDown(self):
        pass

    def test_tag_lex(self):
        lex = interpret("tag[test1]")
        self.assertEqual(len(lex), 2)

        lex = interpret("tag[]")
