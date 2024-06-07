from collections import defaultdict
class Record:
    _known_tags = set()
    _instances = []

    def __init__(self, tags):
        Record.add_known_tags(tags)
        self.tags = tags
        self.connections = defaultdict(list)
        Record._instances.append(self)

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
        return sorted(Record._known_tags)

    @staticmethod
    def add_known_tags(tags):
        for x in tags:
            Record._known_tags.add(x)

    @staticmethod
    def remove_unused_tags():
        all_tags_in_use = {tag for instance in Record._instances for tag in instance.tags}
        Record._known_tags.intersection_update(all_tags_in_use)