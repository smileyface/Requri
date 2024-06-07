from collections import defaultdict
class Record:
    _known_tags = set()

    def __init__(self, tags):
        self.tags = tags
        self.connections = defaultdict(list)
        Record.add_known_tags(tags)

    def connect(self, connect):
        """
        Connects the given object to the current object.

        Args:
            connect: The object to connect to the current object.
        """
        if not isinstance(connect, Record):
            raise TypeError("The `connect` parameter must be an instance of `Record`.")
        self.connections[type(connect)].append(connect)

    @staticmethod
    def get_known_tags():
        return list(Record._known_tags)

    @staticmethod
    def add_known_tags(tags):
        for x in tags:
            Record._known_tags.add(x)
