from revotool import modx


m = modx.MODXClient('http://localhost:8090', 'admin', 'password')


def test_login():
    assert len(m.http.cookies['PHPSESSID']) == 32
    assert len(m.modauth) == 52
    assert m.modauth[:4] == 'modx'


def test_getElements():
    tpls = m.getElements('template')
    assert tpls[0]['classKey'] == 'modCategory'


def test_getElement():
    tpl = m.getElement('template', 1)
    assert tpl['id'] == 1


def test_updateElement():
    tpl = m.updateElement('template', 1, {
        'templatename': 'BaseTemplate',
        'description': 'TemplateBase'
    })
    assert tpl['description'] == 'TemplateBase'
