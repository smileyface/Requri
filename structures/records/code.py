from structures.lists.code_list import _code_list, signature_to_id_map
from structures.records.record import Record


class Code_Location:
    DEFINITION = 0
    DECLARATION = 1

    def __init__(self, type, file, begin, end):
        self.type = type
        self.file = file
        self.begin = begin
        self.end = end


class Code(Record):
    id_map = []
    id_range_max = 1000

    def __init__(self, file, access_level, class_name, name, arguments, func_begin, func_end, definition,
                 unique_id=None):
        super()
        self.access_level = access_level
        self.class_name = class_name
        self.name = name
        self.arguments = arguments
        self.func_begin = func_begin
        self.func_end = func_end
        self.call_list = []
        self.connections = dict()
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

    def connect(self, type, connect):
        if not type in self.connections.keys():
            self.connections[type] = [connect]
        else:
            self.connections[type].append(connect)

    def __str__(self):
        return self.signature

    def to_json(self):
        definition = ""
        declaration = ""
        if self.definition:
            definition = self.definition.path
        if self.declaration:
            declaration = self.declaration.path
        call_list = []
        for x in self.call_list:
            call_list.append(str(x))
        return {"id": self._unique_id, "definition": definition, "declaration": declaration,
                "access": self.access_level, "class": self.class_name,
                "name": self.name, "arguments": self.arguments, "begin": self.func_begin, "end": self.func_end,
                "call_list": call_list}


def expand_from_json(param):
    for x in param:
        _code_list[x["id"]] = Code(x["declaration"], x["access"], x["class"], x["name"], x["arguments"], x["begin"],
                                   x["end"], x["id"], False)
        _code_list[x["id"]].definition = x["definition"]
        signature_to_id_map[_code_list[x["id"]].signature] = _code_list[x["id"]].unique_id
