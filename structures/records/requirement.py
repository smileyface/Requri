from structures.records.record import Record
from structures.requirement_id import RequirementId


class Requirement(Record):
    def __init__(self, section, sub, title, text, tags, unique_id=None):
        super().__init__(tags)
        self._unique_id = RequirementId(section, sub, unique_id)
        self.text = text.strip()
        self.title = title

    def connect(self, connection):
        if type(connection).__name__() == "Requirement":
            self.connections["Supporting Requirement"] = connection
        elif type(connection).__name__() == "Code":
            self.connections["Implementation"] = connection
        else:
            super().connect(connection)

    @property
    def unique_id(self):
        return self._unique_id

    def __str__(self):
        if self.title != "":
            return self.title
        else:
            self.text[:20]

    def to_string(self):
        string = self.unique_id.to_string() + ": " + self.title + "\n" + self.text + "\n\t"
        for x in self.tags:
            string += "#" + x + ", "
        return string

    def to_json(self):
        json = {"id": self._unique_id.to_json(), "title": self.title, "text": self.text, "tags": self.tags}
        return json
