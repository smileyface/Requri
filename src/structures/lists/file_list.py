from typing import List
from src.structures.source_file import File

# A list to store the File objects
_source_file_list: List[File] = []


def add_file(file: File) -> None:
    """
    Adds a File object to the list if it is not a duplicate and has a valid path.

    Parameters:
    file (File): The File object to be added.

    Returns:
    None
    """
    # Ignore files with empty paths
    if not file.path:
        return

    # Ignore duplicate files by checking if a file with the same path already exists
    for existing_file in _source_file_list:
        if existing_file.path == file.path:
            return

    # If the file is valid and not a duplicate, add it to the list
    _source_file_list.append(file)


def get_file_lists() -> List[File]:
    """
    Returns the list of File objects.

    Returns:
    List[File]: The list containing all added File objects.
    """
    return _source_file_list


def clear_file_list() -> None:
    """
    Clears the list of File objects.

    Returns:
    None
    """
    _source_file_list.clear()
