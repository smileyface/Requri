_req_map = {}



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


def add_requirement(requirement):
    _req_map.append(requirement)


def get_requirement_map():
    return _req_map


def clear_list():
    _req_map.map.clear()
