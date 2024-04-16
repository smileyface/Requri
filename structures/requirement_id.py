class RequirementId:
    id_map = dict()

    def __init__(self, section, sub):
        self.section = section
        self.sub = sub
        self.unique_id = self._get_unique_id();

    def _get_unique_id(self):
        location = (self.section, self.sub)
        if location not in self.id_map.keys():
            RequirementId.id_map[location] = 0

        unique_id = RequirementId.id_map[location]
        RequirementId.id_map[location] += 1
        return unique_id

    def to_string(self):
        return self.section + "-" + self.sub + "-" + str(self.unique_id)

    def to_json(self):
        return {"section": self.section, "subsection": self.sub, "unique_id": self.unique_id}

    def from_json(self, json):
        self.section = json["section"]
        self.sub = json["subsection"]
        self.unique_id = json["unique_id"]
        if (self.section, self.sub) not in RequirementId.id_map.keys():
            RequirementId.id_map[(self.section, self.sub)] = self.unique_id + 1
        if RequirementId.id_map[(self.section, self.sub)] <= self.unique_id:
            RequirementId.id_map[(self.section, self.sub)] = self.unique_id + 1