from unittest.mock import MagicMock

import pytest

from src.structures.lists.file_list import add_file, get_file_lists, clear_file_list
from src.structures.source_file import File


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

    def test_add_file(self):
        """Test adding a file to the list."""
        mock_file = MagicMock(spec=File)
        mock_file.path = "test_file.txt"

        # Add a file
        add_file(mock_file)

        # Verify the file list contains the added file
        file_list = get_file_lists()
        assert len(file_list) == 1, "Expected one file in the list."
        assert file_list[0] == mock_file, "Expected the list to contain the mocked File object."

    def test_ignore_empty_file_name(self):
        """Test that empty file names are ignored."""
        mock_file = MagicMock(spec=File)
        mock_file.path = ""

        # Try to add an empty file name
        add_file(mock_file)

        # Verify the file list is still empty
        file_list = get_file_lists()
        assert len(file_list) == 0, "Expected the file list to be empty when an empty file name is added."

    def test_ignore_duplicate_files(self):
        """Test that duplicate files are ignored."""
        mock_file = MagicMock(spec=File)
        mock_file.path = "duplicate_file.txt"

        # Add the same file twice
        add_file(mock_file)
        add_file(mock_file)

        # Verify the file list contains only one instance of the file
        file_list = get_file_lists()
        assert len(file_list) == 1, "Expected only one file in the list (duplicate should be ignored)."
        assert file_list[0] == mock_file

    def test_add_multiple_files(self):
        """Test adding multiple files to the list."""
        mock_file1 = MagicMock(spec=File)
        mock_file1.path = "test_file1.txt"
        mock_file2 = MagicMock(spec=File)
        mock_file2.path = "test_file2.txt"

        # Add multiple files
        add_file(mock_file1)
        add_file(mock_file2)

        # Verify the file list contains all added files
        file_list = get_file_lists()
        assert len(file_list) == 2, "Expected two files in the list."
        assert file_list[0] == mock_file1
        assert file_list[1] == mock_file2

    def test_clear_file_list(self):
        """Test clearing the file list."""
        mock_file = MagicMock(spec=File)
        mock_file.path = "test_file.txt"

        # Add a file to ensure the list is not empty
        add_file(mock_file)

        # Clear the file list
        clear_file_list()

        # Verify the file list is empty
        file_list = get_file_lists()
        assert len(file_list) == 0, "Expected the file list to be empty after clearing."
