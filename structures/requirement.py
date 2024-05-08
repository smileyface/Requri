from structures.requirement_id import RequirementId

_known_tags = set()


def get_known_tags():
    return list(_known_tags)


def add_known_tags(tags):
    global _known_tags
    for x in tags:
        _known_tags.add(x)


class Requirement:
    def __init__(self, section, sub, title, text, tags, unique_id=None):
        self._unique_id = RequirementId(section, sub, unique_id)
        self.text = text.strip()
        self.tags = tags
        self.title = title
        self.connections = dict()
        add_known_tags(tags)

    @property
    def unique_id(self):
        return self._unique_id

    def connect(self, type, connect):
        if not type in self.connections.keys():
            self.connections[type] = [connect]
        else:
            self.connections[type].append(connect)

    def to_string(self):
        string = self.unique_id.to_string() + ": " + self.title + "\n" + self.text + "\n\t"
        for x in self.tags:
            string += "#" + x + ", "
        return string

    def to_json(self):
        json = {"id": self._unique_id.to_json(), "title": self.title, "text": self.text, "tags": self.tags}
        return json
