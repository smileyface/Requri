class Record:
    _known_tags = set()

    def __init__(self, tags):
        self.tags = tags
        self.connections = dict()
        Record.add_known_tags(tags)

    def connect(self, connect):
        if not type(connect) in self.connections.keys():
            self.connections[type(connect)] = [connect]
        else:
            self.connections[type(connect)].append(connect)

    @staticmethod
    def get_known_tags():
        return list(Record._known_tags)

    @staticmethod
    def add_known_tags(tags):
        for x in tags:
            Record._known_tags.add(x)
