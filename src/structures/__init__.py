from src.structures.lists import requirement_list
from src.structures.lists import code_list


def get_lists():
    all_list = []
    if len(requirement_list.get_requirement_map()) != 0:
        all_list.extend(requirement_list.get_requirement_list())
    if len(code_list.get_code_list()) != 0:
        all_list.extend(code_list.get_code_list())
    return all_list
