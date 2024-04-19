from structures import requirement_list

_name = ""
_save_file = ""


def get_name():
    return _name

def set_name(name):
    _name = name


def get_save_file():
    return _save_file


def set_save_file(file_directory):
    global _save_file
    _save_file = file_directory


def generate_save_file():
    save_file = {"filename": _name, "req": {}, "code": {}, "test": {}}
    req_map = requirement_list.get_requirement_map()
    req = []
    for map_key in req_map.keys():
        for requirement in req_map[map_key].values():
            req.append(requirement.to_json())
    save_file["req"] = req
    return save_file


def expand_save_file(all_the_things):
    global _name
    _name = all_the_things["filename"]
    requirement_list.expand_from_json(all_the_things["req"])