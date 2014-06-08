from revotool.common import EXTS, WithMapping


class Puller(WithMapping):

    def __init__(self, remote_name):
        self.remote_name = remote_name
        self.mapping = {}

    def _process_content(self, el):
        res = el['content']
        if len(res) == 0:
            return res
        if res[-1] != '\n':
            res += '\n'
        if el['type'] == 'plugin' or el['type'] == 'snippet':
            res = '<?php\n' + res
        return res

    def _process(self, tp, path, elements):
        for el in elements:
            if el['classKey'] == 'modCategory':
                children = self.modxclient.getElements(tp, node=el['id'])
                newpath = path + el['data']['category'] + '/'
                self._process(tp, newpath, children)
            else:
                filepath = path + el['name'] + '.' + EXTS[tp]
                el.update(self.modxclient.getElement(tp, el['pk']))
                el['content'] = self._process_content(el)
                self.fs.write(filepath, el['content'])
                self.mapping[filepath] = el['pk']

    def pull(self, tp):
        self._process(tp, tp + 's/', self.modxclient.getElements(tp))
        self._write_mapping()
