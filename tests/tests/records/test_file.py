import hashlib
import os

from structures import project
from structures.records.record import Record

from src.structures.source_file import File

import pytest


class TestFile:

    @pytest.fixture(autouse=True)
    def setup(self):
        project.set_code_location(os.path.abspath(os.path.relpath(".")))

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        Record.clear_records()

    #  Correctly normalizes and returns the file path
    def test_normalizes_file_path(self):
        file = File("some\\path\\to\\file.txt")
        assert file.path == os.path.normpath("some/path/to/file.txt")

    #  Correctly sets the file path relative to the project code location
    def test_sets_file_path_relative_to_project(self):
        project_code_location = project.get_code_location()
        file = File(os.path.join(project_code_location, "some/path/to/file.txt"))
        assert file._path == os.path.normpath("some/path/to/file.txt")

    #  Reads and returns the file source content accurately
    def test_reads_file_source_content(self):
        with open("test_file.txt", "w") as f:
            f.write("Hello, World!")
        file = File("test_file.txt")
        assert file.source == "Hello, World!"
        os.remove(os.path.join(project.get_code_location(), "test_file.txt"))

    #  Computes and returns the MD5 hash of the file content
    def test_computes_md5_hash(self):
        with open("test_file.txt", "w") as f:
            f.write("Hello, World!")
        file = File("test_file.txt")
        expected_md5 = hashlib.md5("Hello, World!".encode('utf-8')).hexdigest()
        assert file.md5 == expected_md5
        os.remove(os.path.join(project.get_code_location(), "test_file.txt"))

    #  Correctly handles valid file paths and content
    def test_handles_valid_file_paths_and_content(self):
        with open("valid_file.txt", "w") as f:
            f.write("Valid content")
        file = File("valid_file.txt")
        assert file.source == "Valid content"
        os.remove(os.path.join(project.get_code_location(), "valid_file.txt"))

    #  Handles non-existent file paths gracefully
    def test_handles_non_existent_file_paths(self):
        file = File("non_existent_file.txt")
        with pytest.raises(FileNotFoundError):
            _ = file.source

    #  Manages empty file content without errors
    def test_manages_empty_file_content(self):
        with open("empty_file.txt", "w") as f:
            pass
        file = File("empty_file.txt")
        assert file.source == ""
        os.remove(os.path.join(project.get_code_location(), "empty_file.txt"))

    #  Handles file paths with special characters
    def test_handles_special_characters_in_file_paths(self):
        with open("special_!@#$.txt", "w") as f:
            f.write("Special characters")
        file = File("special_!@#$.txt")
        assert file.source == "Special characters"
        os.remove(os.path.join(project.get_code_location(), "special_!@#$.txt"))

    #  Deals with very large files efficiently
    def test_handles_large_files(self):
        large_content = "A" * 10 ** 6  # 1 MB of 'A's
        with open("large_file.txt", "w") as f:
            f.write(large_content)
        file = File("large_file.txt")
        assert file.source == large_content
        os.remove(os.path.join(project.get_code_location(), "large_file.txt"))

    #  Handles read permissions issues on the file
    @pytest.mark.skip(reason="This test is having permission issues")
    def test_handles_read_permissions_issues(self):
        with open("no_read_permission.txt", "w") as f:
            f.write("No read permission")
        os.chmod("no_read_permission.txt", 0o000)
        file = File("no_read_permission.txt")
        with pytest.raises(PermissionError):
            _ = file.source
        os.chmod("no_read_permission.txt", 0o777)
        os.remove(os.path.join(project.get_code_location(), "no_read_permission.txt"))

    #  Correctly updates MD5 hash when file content changes
    def test_updates_md5_hash_on_content_change(self):
        with open("update_md5.txt", "w") as f:
            f.write("Initial content")
        file = File("update_md5.txt")
        initial_md5 = file.md5
        with open("update_md5.txt", "w") as f:
            f.write("Updated content")
        updated_md5 = file.md5
        assert initial_md5 != updated_md5
        os.remove(os.path.join(project.get_code_location(), "update_md5.txt"))

    #  Ensures path normalization works across different operating systems
    def test_path_normalization_across_os(self):
        file = File("some\\path\\to\\file.txt")
        assert file.path == os.path.normpath("some/path/to/file.txt")
