from structures.requirement import Requirement

_req_map = {}


def update(unique_id, updated):
    _req_map[(unique_id.section, unique_id.sub)][
        unique_id.unique_id] = updated


def append(requirement):
    if (requirement.unique_id.section, requirement.unique_id.sub) not in _req_map:
        _req_map[(requirement.unique_id.section, requirement.unique_id.sub)] = {}
    _req_map[(requirement.unique_id.section, requirement.unique_id.sub)][
        requirement.unique_id.unique_id] = requirement


def remove(requirement):
    del _req_map[(requirement.unique_id.section, requirement.unique_id.sub)][requirement.unique_id.unique_id]


def get_section_lists():
    thing = set()
    for x in _req_map:
        thing.add(x[0])
    return list(thing)


def get_subsection_lists(section):
    thing = set()
    for x in _req_map:
        if x[0] == section:
            thing.add(x[1])
    return list(thing)


def get_requirement_from_index_string(string):
    id_split = string.split("-")
    return _req_map[(id_split[0], id_split[1])][int(id_split[2])]


def expand_from_json(json_array):
    for req in json_array["req"]:
        requirement = Requirement("", "", "", "", [])
        requirement.from_json(req)
        append(requirement)


def add_requirement(requirement):
    _req_map.append(requirement)

def get_requirement_map():
    return _req_map


def clear_list():
    _req_map.clear()
