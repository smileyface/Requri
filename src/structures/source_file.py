import os.path
import hashlib

from src.structures import project


class File:
    def __init__(self, path):
        self._md5 = 0
        self._path = ""
        self._source = ""
        self.path = path
        self.functions = []

    @property
    def path(self):
        return os.path.normpath(self._path)

    @path.setter
    def path(self, _path):
        _path = os.path.normpath(_path)
        self._path = os.path.relpath(_path, project.get_code_location())

    @property
    def full_path(self):
        return os.path.normpath(project.get_code_location() + "\\" + self._path)

    @property
    def source(self):
        with open(self.full_path) as f:
            content = f.readlines()
        return "".join(content)

    @property
    def md5(self):
        return hashlib.md5(self.source.encode('utf-8')).hexdigest()
