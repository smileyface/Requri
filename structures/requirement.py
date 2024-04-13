from structures.requirement_id import RequirementId


class Requirement:
    def __init__(self, section, sub, title, text, tags):
        self._unique_id = RequirementId(section, sub)
        self.text = text
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



