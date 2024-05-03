from structures.code_list import code_list, signature_to_id_map


class Code:
    id_map = []
    id_range_max = 1000

    def __init__(self, file, access_level, class_name, name, arguments, func_begin, func_end, definition,
                 unique_id=None):
        self.access_level = access_level
        self.class_name = class_name
        self.name = name
        self.arguments = arguments
        self.func_begin = func_begin
        self.func_end = func_end
        self.call_list = []
        if definition:
            self.definition = file
            self.declaration = None
        else:
            self.definition = None
            self.declaration = file
        self._unique_id = None
        if unique_id is not None:
            self.unique_id = unique_id

    @property
    def unique_id(self):
        if self._unique_id is None:
            self._unique_id = self._create_unique_id()
        return self._unique_id

    @unique_id.setter
    def unique_id(self, id):
        if id < 0 or id > Code.id_range_max:
            raise ValueError("ID out of range")
        elif id in Code.id_map:
            raise ValueError("Non Unique ID")
        else:
            Code.id_map.append(id)
            self._unique_id = id

    @property
    def signature(self):
        return f"{self.class_name}::{self.name}({', '.join(self.arguments)})"

    def _create_unique_id(self):
        for x in range(0, self.id_range_max):
            if x not in Code.id_map:
                Code.id_map.append(x)
                return x

    def to_json(self):
        return {"id": self._unique_id, "definition": self.definition, "declaration": self.declaration,
                "access": self.access_level, "class": self.class_name,
                "name": self.name, "arguments": self.arguments, "begin": self.func_begin, "end": self.func_end,
                "call_list": self.call_list}


def expand_from_json(param):
    for x in param:
        code_list[x["id"]] = Code(x["location"], x["access"], x["class"], x["name"], x["arguments"], x["begin"],
                                  x["end"], x["id"], False)
        code_list[x["id"]].definition = x["definition"]
        signature_to_id_map[code_list[x["id"]].signature] = code_list[x["id"]].unique_id
