from structures.requirement_id import RequirementId


class Requirement:
    def __init__(self, section, sub, title, text, tags):
        self._unique_id = RequirementId(section, sub)
        self.text = text.strip()
        self.tags = tags
        self.title = title

    @property
    def unique_id(self):
        return self._unique_id

    def to_string(self):
        string = self.unique_id.to_string() + ": " + self.title + "\n" + self.text +"\n\t"
        for x in self.tags:
            string += "#" + x + ", "
        return string

    def to_json(self):
        return {"id": self.unique_id.to_json(), "text": self.text, "tags": self.tags, "title": self.title}

    def from_json(self, json):
        self.unique_id.from_json(json["id"])
        self.text = json["text"]
        self.tags = json["tags"]
        self.title = json["title"]

