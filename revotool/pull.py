from revotool.common import EXTS, WithMapping


class Puller(WithMapping):

    def __init__(self, remote_name):
        self.remote_name = remote_name
        self.mapping = {}

    def _process(self, tp, path, elements):
        for el in elements:
            if el['classKey'] == 'modCategory':
                children = self.modxclient.getElements(tp, node=el['id'])
                newpath = path + el['data']['category'] + '/'
                self._process(tp, newpath, children)
            else:
                filepath = path + el['name'] + '.' + EXTS[tp]
                full_el = self.modxclient.getElement(tp, el['pk'])
                self.fs.write(filepath, full_el['content'])
                self.mapping[filepath] = el['pk']

    def pull(self, tp):
        self._process(tp, tp + 's/', self.modxclient.getElements(tp))
        self._write_mapping()
