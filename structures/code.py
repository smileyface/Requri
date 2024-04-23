code_list = dict()


def append(code):
    global code_list
    code_list[code.unique_id] = code

class Code:
    id_map = []
    id_range_max = 1000

    def __init__(self, url, access_level, class_name, name, arguments, func_begin, func_end, unique_id=None):
        self.location = url
        self.access_level = access_level
        self.class_name = class_name
        self.name = name
        self.argument = arguments
        self.func_begin = func_begin
        self.func_end = func_end
        self.call_list = []
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
        return f"{self.access_level}::{self.class_name}::{self.name}({', '.join(self.argument)})"

    def _create_unique_id(self):
        for x in range(0, self.id_range_max):
            if x not in Code.id_map:
                Code.id_map.append(x)
                return x

    def to_json(self):
        return {"id": self._unique_id, "url": self.location, "signature": self.name}