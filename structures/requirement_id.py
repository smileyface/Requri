class RequirementId:
    id_map = dict()
    id_range_max = 99999

    def __init__(self, section, sub, unique_id=None):
        self.section = section
        self.sub = sub
        self._unique_id = None
        if unique_id is not None:
            self.unique_id = unique_id

    def __del__(self):
        self.reset_unique_id()

    @property
    def unique_id(self):
        if self._unique_id is None:
            self._unique_id = self._create_unique_id()
        return self._unique_id

    @unique_id.setter
    def unique_id(self, id):
        location = (self.section, self.sub)
        if location not in self.id_map.keys():
            RequirementId.id_map[location] = [id]
            self._unique_id = id
        elif id < 0 or id > self.id_range_max:
            raise ValueError("ID out of range")
        elif id in RequirementId.id_map[location]:
            raise ValueError("Non Unique ID")
        else:
            RequirementId.id_map[location].append(id)
            self._unique_id = id

    def reset_unique_id(self):
        location = (self.section, self.sub)
        if location in self.id_map:
            RequirementId.id_map.clear()
        self._unique_id = None

    def _create_unique_id(self):
        location = (self.section, self.sub)
        if location not in self.id_map.keys():
            RequirementId.id_map[location] = [0]
            return 0
        else:
            for x in range(0, self.id_range_max):
                if x not in RequirementId.id_map[location]:
                    RequirementId.id_map[location].append(x)
                    return x

    def to_string(self):
        string_to_return = ""
        if self.section != '':
            string_to_return += f"{self.section}-"
        if self.sub != '':
            string_to_return += f"{self.sub}-"

        return string_to_return + str(self.unique_id)

    def to_json(self):
        return {"section": self.section, "sub": self.sub, "id": self._unique_id}
