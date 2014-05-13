import json
import os
from os import path


class FS(object):

    def __init__(self, root):
        self.root = path.abspath(root)

    def write(self, filepath, content):
        fullpath = path.join(self.root, filepath)
        try:
            os.makedirs(path.dirname(fullpath))
        except (OSError, IOError):
            pass
        with open(fullpath, 'w') as f:
            f.write(content)

    def write_data(self, filepath, content):
        return self.write(filepath, json.dumps(content))

    def read(self, filepath):
        fullpath = path.join(self.root, filepath)
        with open(fullpath, 'r') as f:
            return f.read()

    def read_data(self, filepath):
        return json.loads(self.read(filepath))
