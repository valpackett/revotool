import os
from os import path
from revotool.common import WithMapping


def name_key(tp):
    if tp == 'template':
        return 'templatename'
    else:
        return 'name'


class Pusher(WithMapping):

    def __init__(self, remote_name):
        self.remote_name = remote_name
        self.mapping = {}

    def _process(self, tp):
        for root, dirs, files in os.walk(tp + 's/'):
            for filename in files:
                fullpath = path.join(root, filename)
                with open(fullpath, 'r') as f:
                    content = f.read()
                cat_name = path.basename(root)
                category = ''
                if cat_name != tp + 's' and cat_name != '':
                    if cat_name in self.categories:
                        category = self.categories[cat_name]
                    else:
                        raise Exception('Nonexistent category ' + cat_name)
                data = {
                    'content': content,
                    'category': category
                }
                data[name_key(tp)] = path.splitext(filename)[0]
                if fullpath in self.mapping:
                    pk = self.mapping[fullpath]
                    self.modxclient.updateElement(tp, pk, data)
                else:
                    res = self.modxclient.createElement(tp, data)
                    self.mapping[fullpath] = res['id']

    def push(self, tp):
        try:
            self.mapping = self._read_mapping()
        except (IOError, OSError):
            self.mapping = {}
        self.categories = self._read_categories()
        self._process(tp)
        self._write_mapping()

    def _read_categories(self):
        categories = {}
        cats = self.modxclient.getElements('category', node='n_category')
        for cat in cats:
            categories[cat['data']['category']] = cat['pk']
        return categories
