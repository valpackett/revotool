from revotool import modx, pull
from mock import MagicMock


puller = pull.Puller('origin')
puller.modxclient = modx.MODXClient('http://localhost:8090', 'admin',
'password')
puller.fs = MagicMock()


def test_pull():
    puller.pull('template')
    puller.fs.write.assert_called_once_with(
        'templates/TestCat/BaseTemplate.html',
        '<html>[[*content]]</html>')
    puller.fs.write_data.assert_called_once_with(
        '_revotool/origin.template.map.json',
        {'templates/TestCat/BaseTemplate.html': 1})
