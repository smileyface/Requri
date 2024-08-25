import os

# Generated by CodiumAI

from src.structures.records.code_location import Code_Location

import pytest

class TestCodeLocation:

    #  Initializes with valid DEFINITION location type
    def test_initializes_with_valid_definition_location_type(self):
        location = Code_Location(Code_Location.DEFINITION, "example_file.py", 10, 20)
        assert location.location_type == Code_Location.DEFINITION
        assert location.file == os.path.abspath("example_file.py")
        assert location.begin == 10
        assert location.end == 20

    #  Initializes with valid DECLARATION location type
    def test_initializes_with_valid_declaration_location_type(self):
        location = Code_Location(Code_Location.DECLARATION, "example_file.py", 30, 40)
        assert location.location_type == Code_Location.DECLARATION
        assert location.file == os.path.abspath("example_file.py")
        assert location.begin == 30
        assert location.end == 40

    #  Converts relative file path to absolute path
    def test_converts_relative_file_path_to_absolute_path(self):
        relative_path = "example_file.py"
        location = Code_Location(Code_Location.DEFINITION, relative_path, 10, 20)
        assert location.file == os.path.abspath(relative_path)

    #  Correctly sets begin and end values when valid
    def test_correctly_sets_begin_and_end_values_when_valid(self):
        location = Code_Location(Code_Location.DEFINITION, "example_file.py", 10, 20)
        assert location.begin == 10
        assert location.end == 20

    #  Raises error for invalid location type
    def test_raises_error_for_invalid_location_type(self):
        with pytest.raises(ValueError, match="Invalid type parameter"):
            Code_Location(2, "example_file.py", 10, 20)

    #  Raises error when begin is negative
    def test_raises_error_when_begin_is_negative(self):
        with pytest.raises(ValueError, match="Invalid begin or end values"):
            Code_Location(Code_Location.DEFINITION, "example_file.py", -1, 20)

    #  Raises error when end is negative
    def test_raises_error_when_end_is_negative(self):
        with pytest.raises(ValueError, match="Invalid begin or end values"):
            Code_Location(Code_Location.DEFINITION, "example_file.py", 10, -1)

    #  Raises error when begin is greater than end
    def test_raises_error_when_begin_is_greater_than_end(self):
        with pytest.raises(ValueError, match="Invalid begin or end values"):
            Code_Location(Code_Location.DEFINITION, "example_file.py", 20, 10)

    #  Handles empty file path gracefully
    def test_handles_empty_file_path_gracefully(self):
        location = Code_Location(Code_Location.DEFINITION, "", 10, 20)
        assert location.file == os.path.abspath("")

    #  Handles non-existent file path gracefully
    def test_handles_non_existent_file_path_gracefully(self):
        non_existent_path = "non_existent_file.py"
        location = Code_Location(Code_Location.DEFINITION, non_existent_path, 10, 20)
        assert location.file == os.path.abspath(non_existent_path)

    #  Ensures DEFINITION and DECLARATION constants are correctly set
    def test_ensures_definition_and_declaration_constants_are_correctly_set(self):
        assert Code_Location.DEFINITION == 0
        assert Code_Location.DECLARATION == 1

    #  Validates file path normalization
    def test_validates_file_path_normalization(self):
        relative_path = "./example_file.py"
        normalized_path = os.path.normpath(relative_path)
        location = Code_Location(Code_Location.DEFINITION, relative_path, 10, 20)
        assert location.file == os.path.abspath(normalized_path)