from src.structures.records.requirement import Requirement
from src.structures.requirement_id import RequirementId

_req_map = {}


def update(unique_id, section, sub, title, text, tags):
    # Update section and subsection
    if not unique_id.section == section or not unique_id.sub == sub:
        append(Requirement(section, sub, title, text, tags))
        _req_map.pop((unique_id.section, unique_id.sub))
    _req_map[(unique_id.section, unique_id.sub)][
        unique_id.unique_id].title = title
    _req_map[(unique_id.section, unique_id.sub)][
        unique_id.unique_id].text = text
    _req_map[(unique_id.section, unique_id.sub)][
        unique_id.unique_id].tags = tags


def append(requirement):
    if (requirement.unique_id.section, requirement.unique_id.sub) not in _req_map:
        _req_map[(requirement.unique_id.section, requirement.unique_id.sub)] = {}
    _req_map[(requirement.unique_id.section, requirement.unique_id.sub)][
        requirement.unique_id.unique_id] = requirement


def map_is_empty():
    return _req_map == {}


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
    _req_map[requirement.unique_id] = requirement


def get_requirement_map():
    return _req_map


def get_requirement_list():
    list_of_map = []
    for x in _req_map.keys():
        list_of_map.extend(_req_map[x].values())
    return list_of_map

def expand_from_json(all_the_things):
    for x in all_the_things:
        req = Requirement(x["id"]['section'], x["id"]["sub"], x["title"], x["text"], x["tags"], x["id"]["id"])
        append(req)


def clear():
    _req_map.clear()
    RequirementId.clear_id_map()



def get(unique_id):
    return _req_map[unique_id.key][unique_id.unique_id]
