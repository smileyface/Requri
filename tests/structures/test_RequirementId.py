# Generated by CodiumAI

import pytest

from structures.records.record import Record
from structures.requirement_id import RequirementId


class TestRequirementId:

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        Record.clear_records()

    #  Creating a RequirementId instance with a unique ID
    def test_create_instance_with_unique_id(self):
        req_id = RequirementId("section1", "sub1", 1)
        assert req_id.unique_id == 1
        assert RequirementId.id_map[("section1", "sub1")] == {1}

    #  Creating a RequirementId instance without a unique ID and auto-generating one
    def test_create_instance_without_unique_id(self):
        req_id = RequirementId("section2", "sub2")
        assert req_id.unique_id == 0
        assert RequirementId.id_map[("section2", "sub2")] == {0}

    #  Getting the unique_id property when it is already set
    def test_get_unique_id_when_set(self):
        req_id = RequirementId("section3", "sub3", 3)
        assert req_id.unique_id == 3

    #  Setting the unique_id property with a valid ID
    def test_set_unique_id_valid(self):
        req_id = RequirementId("section4", "sub4")
        req_id.unique_id = 4
        assert req_id.unique_id == 4
        assert RequirementId.id_map[("section4", "sub4")] == {4}

    #  Converting a RequirementId instance to a string
    def test_to_string_conversion(self):
        req_id = RequirementId("section5", "sub5", 5)
        assert str(req_id) == "section5-sub5-5"

    #  Converting a RequirementId instance to JSON
    def test_to_json_conversion(self):
        req_id = RequirementId("section6", "sub6", 6)
        assert req_id.to_json() == {"section": "section6", "sub": "sub6", "id": 6}

    #  Setting the unique_id property with an ID out of range
    def test_set_unique_id_out_of_range(self):
        with pytest.raises(ValueError, match="ID out of range"):
            req_id = RequirementId("section7", "sub7")
            req_id.unique_id = 100000

    #  Setting the unique_id property with a non-unique ID
    def test_set_non_unique_id(self):
        req_id1 = RequirementId("section8", "sub8", 8)
        with pytest.raises(ValueError, match="Non Unique ID"):
            req_id2 = RequirementId("section8", "sub8", 8)

    #  Creating a RequirementId instance with a section and sub that already exist in id_map
    def test_create_instance_existing_section_sub(self):
        req_id1 = RequirementId("section9", "sub9", 9)
        req_id2 = RequirementId("section9", "sub9")
        assert req_id2.unique_id == 0
        assert RequirementId.id_map[("section9", "sub9")] == {9, 0}

    #  Deleting a RequirementId instance and ensuring the ID is removed from id_map
    def test_delete_instance_removes_id_from_map(self):
        req_id = RequirementId("section10", "sub10", 10)
        del req_id
        assert 10 not in RequirementId.id_map[("section10", "sub10")]

    #  Deleting a RequirementId instance and ensuring the ID is removed from id_map
    def test_delete_instance_removes_id_from_map(self):
        req_id = RequirementId("section11", "sub11", 11)
        del req_id
        assert 11 not in RequirementId.id_map[("section11", "sub11")]

    #  Handling the case where the id_map is empty after resetting
    def test_handle_empty_id_map_after_reset(self):
        # Reset id_map
        RequirementId.id_map = {}

        # Ensure id_map is empty
        assert RequirementId.id_map == {}

    #  Handling the case where the id_map is empty
    def test_handle_empty_id_map(self):
        assert RequirementId.id_map == {}

    #  Resetting the unique_id and ensuring it is removed from id_map
    def test_unique_id_removal_on_from_map_on_delete(self):
        # Create an instance of RequirementId
        req_id = RequirementId(section="A", sub="1", new_unique_id=10)

        # Ensure the unique ID is set correctly
        assert req_id.unique_id == 10

        # Ensure the unique ID is in the id_map
        assert 10 in RequirementId.id_map[("A", "1")]

        # Delete the instance
        del req_id

        # Ensure the unique ID is removed from the id_map
        assert 10 not in RequirementId.id_map.get(("A", "1"))

