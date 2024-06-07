import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict

from structures.lists.code_list import _code_list, signature_to_id_map
from structures.records.code_location import Code_Location
from structures.records.record import Record


@dataclass
class Code(Record):
    id_map = set()
    id_range_max = 1000
    file: str
    access_level: str
    class_name: str
    name: str
    arguments: List[str]
    func_begin: str
    func_end: str
    definition: Optional[Code_Location] = None
    declaration: Optional[Code_Location] = None
    _unique_id: Optional[int] = field(default=None, init=False)  # Exclude from __init__
    call_list: List = field(default_factory=list)
    connections: Dict = field(default_factory=dict)
    id: Optional[int] = None  # Add this line

    def __post_init__(self):
        if self.id is None:
            self._unique_id = self._create_unique_id()
        else:
            self.unique_id = self.id


    id_map = set()
    id_range_max = 1000

    @property
    def unique_id(self):
        if self._unique_id is None:
            self._unique_id = self._create_unique_id()
        return self._unique_id

    @unique_id.setter
    def unique_id(self, new_id):
        if new_id < 0 or new_id > Code.id_range_max:
            raise ValueError("ID out of range")
        elif new_id in Code.id_map:
            raise ValueError("Non Unique ID")
        else:
            Code.id_map.add(new_id)
            self._unique_id = new_id

    @property
    def signature(self):
        return f"{self.class_name}::{self.name}({', '.join(self.arguments)})"

    def _create_unique_id(self):
        for x in range(0, self.id_range_max):
            if x not in Code.id_map:
                Code.id_map.add(x)
                return x

    def connect(self, type, connect):
        self.connections.setdefault(type, []).append(connect)

    def __str__(self):
        return self.signature

    def __del__(self):
        if self._unique_id is not None and self._unique_id in Code.id_map:
            Code.id_map.remove(self._unique_id)

    def to_json(self):
        definition = ""
        declaration = ""
        if self.definition:
            definition = self.definition.file
        if self.declaration:
            declaration = self.declaration.file
        call_list = []
        for x in self.call_list:
            call_list.append(str(x))
        return {"id": self.unique_id, "definition": definition, "declaration": declaration,
                "access": self.access_level, "class": self.class_name,
                "name": self.name, "arguments": self.arguments, "begin": self.func_begin, "end": self.func_end,
                "call_list": call_list}


def expand_from_json(param):
    for x in param:
        _code_list[x["id"]] = Code(x["declaration"], x["access"], x["class"], x["name"], x["arguments"], x["begin"],
                                   x["end"], x["id"], False)
        _code_list[x["id"]].definition = x["definition"]
        signature_to_id_map[_code_list[x["id"]].signature] = _code_list[x["id"]].unique_id
