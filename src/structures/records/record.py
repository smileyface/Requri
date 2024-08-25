import logging
import threading
from collections import defaultdict
class Record:
    _known_tags = set()
    _instances = []

    def __init__(self, tags):
        Record.add_known_tags(tags)
        self.tags = tags
        self.connections = defaultdict(list)
        Record._instances.append(self)
        Record.remove_unused_tags()

    def __del__(self):
        #todo: remove this record from all connections
        self.remove_tags(self.tags)

    def connect(self, connect):
        """
        Connects the given object to the current object.

        Args:
            connect: The object to connect to the current object.
        """
        if not isinstance(connect, Record):
            raise TypeError("The `connect` parameter must be an instance of `Record`.")
        self.connections[type(connect)].append(connect)

        logging.info(f"{self} connected to {connect}")

    def remove_tags(self, tags):
        for tag in tags:
            if tag in self.tags:
                self.tags.remove(tag)
        Record.remove_unused_tags()

    @staticmethod
    def remove_record(record):
        if record in Record._instances:
            Record._instances.remove(record)

    @staticmethod
    def get_known_tags():
        return sorted(Record._known_tags)

    @staticmethod
    def add_known_tags(tags):
        for x in tags:
            Record._known_tags.add(x)

    @staticmethod
    def remove_unused_tags():
        removed_tags = Record._known_tags.copy()
        with threading.Lock():
            if not Record._instances == []:
                Record._known_tags.intersection_update({tag for instance in Record._instances for tag in instance.tags})
        removed_tags -= Record._known_tags
        if removed_tags:
            logging.info(f"Removed tags: {removed_tags}")

    @staticmethod
    def clear_records():
        for x in Record._instances:
            Record.remove_record(x)