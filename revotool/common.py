EXTS = {
    'template': 'html',
    'chunk': 'html',
    'snippet': 'php',
    'plugin': 'php'
}


class WithMapping(object):

    def _write_mapping(self):
        filepath = '_revotool/{0}.map.json'.format(self.remote_name)
        self.fs.write_data(filepath, self.mapping)

    def _read_mapping(self):
        filepath = '_revotool/{0}.map.json'.format(self.remote_name)
        return self.fs.read_data(filepath)
