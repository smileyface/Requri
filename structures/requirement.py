from structures.requirement_id import RequirementId

_known_tags = set()

def get_known_tags():
    return _known_tags

def add_known_tags(tags):
    global _known_tags
    for x in tags:
        _known_tags.add(x)

class Requirement:
    def __init__(self, section, sub, title, text, tags):
        self._unique_id = RequirementId(section, sub)
        self.text = text.strip()
        self.tags = tags
        self.title = title
        add_known_tags(tags)

    @property
    def unique_id(self):
        return self._unique_id

    def to_string(self):
        string = self.unique_id.to_string() + ": " + self.title + "\n" + self.text +"\n\t"
        for x in self.tags:
            string += "#" + x + ", "
        return string



