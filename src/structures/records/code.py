from dataclasses import dataclass, field
from typing import Optional, List, Dict

from structures.lists import code_manager
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
    func_begin: int
    func_end: int
    definition: Optional[Code_Location] = None
    declaration: Optional[Code_Location] = None
    _unique_id: Optional[int] = field(default=None, init=False)  # Exclude from __init__
    call_list: List = field(default_factory=list)
    connections: Dict = field(default_factory=dict)
    id: Optional[int] = None  # Add this line

    def __post_init__(self):
        super().__init__([])
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

    def __repr__(self):
        return self.signature

    def __del__(self):
        super().__del__()
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


    def to_markdown(self):
        """
        Converts the Code instance to a markdown representation.

        Returns:
            str: A string containing the markdown representation of the Code instance.
        """
        definition = self.definition.file if self.definition else "None"
        declaration = self.declaration.file if self.declaration else "None"
        call_list_str = ", ".join(str(x) for x in self.call_list)

        markdown = f"""
        ### Code: {self.signature}
        
        - **File**: {self.file}
        - **Access Level**: {self.access_level}
        - **Class**: {self.class_name}
        - **Function Name**: {self.name}
        - **Arguments**: {', '.join(self.arguments)}
        - **Function Begin**: {self.func_begin}
        - **Function End**: {self.func_end}
        - **Definition Location**: {definition}
        - **Declaration Location**: {declaration}
        - **Unique ID**: {self.unique_id}
        - **Call List**: {call_list_str}
        - **Connections**: {self.connections}
        
        """
        return markdown.strip()


def expand_from_json(param):
    for x in param:
        code_manager.get_code_list()[x["id"]] = Code(x["declaration"], x["access"], x["class"], x["name"],
                                                     x["arguments"], x["begin"],
                                                     x["end"], x["id"], False)
        code_manager.get_code_list()[x["id"]].definition = x["definition"]
        code_manager.signature_to_id_map[code_manager.get_code_list()[x["id"]].signature] = \
        code_manager.get_code_list()[x["id"]].unique_id
