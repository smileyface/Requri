from src.structures.source_file import File
from src.structures import project

_source_file_list = []


def add_file(file):
    _source_file_list.append(File(project.get_code_location(), file))


def get_file_lists():
    return _source_file_list


def clear_file_list():
    _source_file_list.clear()