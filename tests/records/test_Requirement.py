import logging

import pytest

from structures.records import Code
from structures.records.record import Record
from structures.records.requirement import Requirement


class TestRequirement:

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        Record.clear_records()

    #  Initialization with valid section, sub, title, text, and tags
    def test_initialization_with_valid_data(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])
        assert req.title == "Title1"
        assert req.text == "Text1"
        assert req.tags == ["tag1"]
        assert str(req.unique_id) == "section1-subsection1-0"

    #  Correctly assigns unique_id when provided
    def test_assigns_provided_unique_id(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"], new_unique_id=123)
        assert str(req.unique_id) == "section1-subsection1-123"

    #  Automatically generates unique_id when not provided
    def test_generates_unique_id_when_not_provided(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])
        assert str(req.unique_id) == "section1-subsection1-0"

    #  Connects to another Requirement instance
    def test_connects_to_another_requirement(self):
        req1 = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])
        req2 = Requirement("section2", "subsection2", "Title2", "Text2", ["tag2"])
        req1.connect(req2)
        assert req1.connections[Requirement][0] == req2

    #  Connects to a Code instance
    def test_connects_to_code_instance(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])
        code = Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21)
        req.connect(code)
        assert req.connections[Code][0] == code

    #  Converts to JSON format correctly
    def test_converts_to_json_format_correctly(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"], new_unique_id=123)
        expected_json = {
            "id": {"section": "section1", "sub": "subsection1", "id": 123},
            "title": "Title1",
            "text": "Text1",
            "tags": ["tag1"]
        }
        assert req.to_json() == expected_json

    #  Initialization with empty title and text
    def test_initialization_with_empty_title_and_text(self):
        req = Requirement("section1", "subsection1", "", "", ["tag1"])
        assert req.title == ""
        assert req.text == ""
        assert req.tags == ["tag1"]

    #  Initialization with None as unique_id
    def test_initialization_with_none_unique_id(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"], new_unique_id=None)
        assert str(req.unique_id) == "section1-subsection1-1"

    #  Connecting to an unsupported object type
    def test_connecting_to_unsupported_object_type(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])
        with pytest.raises(TypeError):
            req.connect("unsupported_object")

    #  Handling of duplicate tags
    def test_handling_of_duplicate_tags(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1", "tag1"])
        assert len(set(req.tags)) == 1  # Duplicate tags are consolidated in a set

    #  Handling of maximum length for text and title
    def test_handling_of_maximum_length_for_text_and_title(self):
        long_text = 'a' * 10000
        long_title = 'b' * 1000
        req = Requirement("section1", "subsection1", long_title, long_text, ["tag1"])
        assert req.title == long_title
        assert req.text == long_text

    #  Converts to string representation correctly
    def test_converts_to_string_representation_correctly(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"], new_unique_id=123)
        assert str(req) == "section1-subsection1-123: Title1"

    #  Adds known tags to Record class
    def test_adds_known_tags_to_record_class(self):
        tags = ["tag1", "tag2"]
        req = Requirement("section1", "subsection1", "Title1", "Text1", tags)
        assert set(Record.get_known_tags()) == set(tags)

    #  Retrieves known tags from Record class
    def test_retrieves_known_tags_from_record_class(self):
        tags = ["tag1", "tag2"]
        Record.add_known_tags(tags)
        req = Requirement("section1", "subsection1", "Title1", "Text1", [])
        assert set(req.get_known_tags()) == set(tags)

    #  Strips whitespace from text during initialization
    def test_strips_whitespace_from_text_during_initialization(self):
        req = Requirement("section1", "subsection1", "Title1", "   Text1   ", ["tag1"])
        assert req.text == "Text1"

    #  Converts to string representation correctly with a Code instance connection
    def test_converts_to_string_representation_correctly_with_code_instance(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"], new_unique_id=123)
        code = Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21)
        req.connect(code)
        assert str(req) == "section1-subsection1-123: Title1 (Connected to Class1::method1(arg1, arg2))"

    #  Connects to a Code instance
    def test_connects_to_a_code_instance(self):
        req = Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])
        code = Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21)
        req.connect(code)
        assert req.connections[Code] == [code]
