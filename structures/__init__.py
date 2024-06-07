from structures.lists import requirement_list
from structures.lists import code_manager


def get_lists():
    all_list = []
    if len(requirement_list.get_requirement_map()) != 0:
        all_list.extend(requirement_list.get_requirement_list())
    if len(code_manager.get_code_list()) != 0:
        all_list.extend(code_manager.get_code_list())
    return all_list
