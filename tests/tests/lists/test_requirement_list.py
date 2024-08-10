import pytest
from src.structures.lists.requirement_list import (
    update, append, map_is_empty, remove, get_section_lists,
    get_subsection_lists, get_requirement_from_index_string,
    get_requirement_list, expand_from_json,
    clear, get
)
from src.structures.records.record import Record
from src.structures.records.requirement import Requirement


class TestRequirementList:
    """
    TestRequirementList

    This class contains test cases for the requirement_list module functionality. The tests cover
    various aspects of the module including adding, updating, removing, and retrieving requirements.

    Included Tests:
    ---------------

    1. test_append_and_get
       - Summary: Verify that a requirement can be appended and retrieved correctly.

    2. test_update
       - Summary: Verify that a requirement can be updated correctly.

    3. test_remove
       - Summary: Verify that a requirement can be removed correctly.

    4. test_get_section_lists
       - Summary: Verify that sections can be retrieved correctly.

    5. test_get_subsection_lists
       - Summary: Verify that subsections can be retrieved correctly for a given section.

    6. test_map_is_empty
       - Summary: Verify that the requirement map is empty when it should be.

    7. test_clear_list
       - Summary: Verify that the requirement list can be cleared correctly.

    8. test_expand_from_json
       - Summary: Verify that requirements can be expanded from a JSON structure correctly.

    9. test_clear
       - Summary: Verify that all requirements can be cleared correctly.

    10. test_get_requirement_from_index_string
        - Summary: Verify that a requirement can be retrieved correctly from an index string.
    """

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        Record.clear_records()
        clear()

    def test_append_and_get(self):
        req = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        append(req)
        result = get(req.unique_id)
        assert result == req

    def test_update(self):
        req = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        append(req)
        update(req.unique_id, 'sec1', 'sub1', 'updated_title', 'updated_text', ['tag2'])
        result = get(req.unique_id)
        assert result.title == 'updated_title'
        assert result.text == 'updated_text'
        assert result.tags == ['tag2']

    def test_remove(self):
        req = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        append(req)
        remove(req)
        with pytest.raises(KeyError):
            get(req.unique_id)

    def test_get_section_lists(self):
        req1 = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        req2 = Requirement('sec2', 'sub1', 'title2', 'text2', ['tag2'])
        append(req1)
        append(req2)
        sections = get_section_lists()
        assert 'sec1' in sections
        assert 'sec2' in sections

    def test_get_subsection_lists(self):
        req1 = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        req2 = Requirement('sec1', 'sub2', 'title2', 'text2', ['tag2'])
        append(req1)
        append(req2)
        subsections = get_subsection_lists('sec1')
        assert 'sub1' in subsections
        assert 'sub2' in subsections

    def test_map_is_empty(self):
        clear()
        assert map_is_empty() is True
        req = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        append(req)
        assert map_is_empty() is False

    def test_clear_list(self):
        req = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        append(req)
        clear()
        assert map_is_empty() is True

    def test_expand_from_json(self):
        clear()
        json_data = [
            {
                "id": {"section": "sec1", "sub": "sub1", "id": 1},
                "title": "title1",
                "text": "text1",
                "tags": ["tag1"]
            },
            {
                "id": {"section": "sec2", "sub": "sub2", "id": 2},
                "title": "title2",
                "text": "text2",
                "tags": ["tag2"]
            }
        ]
        expand_from_json(json_data)
        assert len(get_requirement_list()) == 2

    def test_clear(self):
        req = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        append(req)
        clear()
        assert get_requirement_list() == []

    def test_get_requirement_from_index_string(self):
        req = Requirement('sec1', 'sub1', 'title1', 'text1', ['tag1'])
        append(req)
        req_from_index = get_requirement_from_index_string(
            f'{req.unique_id.section}-{req.unique_id.sub}-{req.unique_id.unique_id}')
        assert req_from_index == req
