import unittest

from lexical.search import interpret
from structures.lists import requirement_list
from structures.records.requirement import Requirement


class TestHarness(unittest.TestCase):
    def setUp(self):
        print(f"Running test: {self._testMethodName}")
        # Test cases
        requirements = [
            Requirement('A', 1, 'Test Requirement', 'This is a test requirement.', ['test', 'requirement']),
            Requirement('B', 2, '', 'This requirement has an empty title.', ['empty', 'title', 'test']),
            Requirement('C', 3, 'Long Text',
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut '
                        'labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco '
                        'laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in '
                        'voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
                        'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                        ['long', 'text', 'lorem', 'ipsum']),
            Requirement('D', 4, 'Special Characters', 'This requirement contains special characters: !@#$%^&*()',
                        ['special', 'characters', 'test']),
            Requirement('E', 5, 'Multiple Tags', 'This requirement has multiple tags.', ['tag1', 'tag2', 'tag3']),
            Requirement('F', 6, 'Unique ID', 'This requirement has a unique ID.', ['unique', 'id', 'test'], 12345),
            Requirement('G', 7, 'No Tags', 'This requirement has no tags.', []),
            Requirement('H', 8, 'Tag with Spaces', 'This requirement has a tag with spaces.', ['tag with spaces']),
            Requirement('I', 9, 'Short Title', 'This requirement has a short title.', ['short', 'title', 'test']),
            Requirement('J', 10, 'A Long Title That Exceeds 20 Characters',
                        'This requirement has a long title that exceeds 20 characters.', ['long', 'title', 'test']),
            Requirement('K', 11, 'Empty Text', '', ['empty', 'text', 'test']),
            Requirement('L', 12, 'Only Title', '', ['only', 'title', 'test']),
            Requirement('M', 13, '', 'This requirement has only text.', ['only', 'text', 'test']),
            Requirement('N', 14, 'Title with Special Characters !@#$%^&*()',
                        'This requirement has special characters in the title.',
                        ['special', 'characters', 'title', 'test']),
            Requirement('O', 15, 'Mixed Case Tags', 'This requirement has mixed case tags.', ['Tag1', 'tAg2', 'TaG3']),
        ]
        for x in requirements:
            requirement_list.append(x)

    def tearDown(self):
        requirement_list.clear_list()

    def test_tag_lex(self):
        lex = interpret("tag[requirement]")
        self.assertEqual(len(lex), 1)

    def test_tag_empty_lex(self):
        lex = interpret("tag[]")
        self.assertEqual(len(lex), 14)

    def test_tag_empty_tag_list(self):
        lex = interpret("tag[] tag[requirement]")
        self.assertEqual(len(lex), 14)

    def test_tag_list_tag_empty(self):
        lex = interpret("tag[requirement] tag[]")
        self.assertEqual(len(lex), 14)

    def test_exact_title_lex(self):
        lex = interpret("title[Test Requirement]")
        self.assertTrue(lex[0].title == "Test Requirement")

    def test_append_title_tag_lex(self):
        lex = interpret("tag[test] + title[Multiple Tags]")
        passed = True
        for x in lex:
            if "test" not in x.tags and x.title != "Multiple Tags":
                passed = False

        self.assertTrue(passed)

    def test_title_tag_error_lex(self):
        try:
            interpret("tag[test]title[Multiple Tags]")
        except SyntaxError as e:
            self.assertEqual(e.msg, "Syntax error at: LexToken(TITLE,'title',1,9)")
