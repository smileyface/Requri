import pytest
from src.structures.lists.file_list import add_file, get_file_lists, clear_file_list
from src.structures.source_file import File
from unittest.mock import patch


@pytest.fixture(autouse=True)
def clean_file_list():
    yield  # This is where the test function runs

    # Cleanup after the test
    clear_file_list()


class TestFileList:
    def test_initial_state(self):
        """Test that the file list is initially empty."""
        file_list = get_file_lists()
        assert len(file_list) == 0, "Expected the file list to be empty initially."

    @patch("src.structures.lists.file_list.project.get_code_location")
    @patch("src.structures.lists.file_list.File")
    def test_add_file(self, mock_file, mock_get_code_location):
        """Test adding a file to the list."""
        # Set up the mocks
        mock_get_code_location.return_value = "/mock/path"
        mock_file.return_value = "MockFileObject"

        # Add a file
        add_file("test_file.txt")

        # Verify that File was created with the correct parameters
        mock_file.assert_called_with("/mock/path", "test_file.txt")

        # Verify the file list contains the added file
        file_list = get_file_lists()
        assert len(file_list) == 1, "Expected one file in the list."
        assert (
                file_list[0] == "MockFileObject"
        ), "Expected the list to contain the mocked File object."

    @patch("src.structures.lists.file_list.project.get_code_location")
    @patch("src.structures.lists.file_list.File")
    def test_add_multiple_files(self, mock_file, mock_get_code_location):
        """Test adding multiple files to the list."""
        mock_get_code_location.return_value = "/mock/path"
        mock_file.side_effect = ["MockFileObject1", "MockFileObject2"]

        # Add multiple files
        add_file("test_file1.txt")
        add_file("test_file2.txt")

        # Verify the file list contains all added files
        file_list = get_file_lists()
        assert len(file_list) == 2, "Expected two files in the list."
        assert file_list[0] == "MockFileObject1"
        assert file_list[1] == "MockFileObject2"

    @patch("src.structures.lists.file_list.File")
    def test_clear_file_list(self, mock_file):
        """Test clearing the file list."""
        # Set up the mocks
        mock_file.return_value = "MockFileObject"
        # Add a file to ensure the list is not empty
        add_file("test_file.txt")

        # Clear the file list
        clear_file_list()

        # Verify the file list is empty
        file_list = get_file_lists()
        assert len(file_list) == 0, "Expected the file list to be empty after clearing."
