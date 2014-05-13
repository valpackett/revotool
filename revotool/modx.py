import re
import requests


RE_AUTH = re.compile('.*auth: ?"([^"]+)".*', re.DOTALL)


class MODXException(Exception):
    pass


class MODXClient(object):

    def __init__(self, host, username, password):
        if host[0] == 'h':
            self.host = host
        else:
            self.host = 'http://' + host
        self.http = requests.Session()
        res = self.http.post(self.host + '/manager', data={
            'login_context': 'mgr',
            'modahsh': '',
            'username': username,
            'password': password,
            'login': '1'
        })
        try:
            self.modauth = RE_AUTH.match(res.text).groups()[0]
        except AttributeError:
            raise MODXException("Wrong password OR something's broken")

    def _post(self, url, params={}, data={}):
        res = self.http.post(self.host + url, params=params, data=data).json()
        if isinstance(res, dict):
            if not res['success']:
                raise MODXException(str(res['data']))
        return res

    def getElements(self, tp, node=None):
        if not node:
            node = 'n_type_' + tp
        return self._post('/connectors/element/index.php',
        params={
            'action': 'getNodes',
            'id': node,
            'type': tp
        }, data={
            'currentElement': '0',
            'currentAction': '0',
            'action': 'getNodes',
            'node': node,
            'HTTP_MODAUTH': self.modauth
        })

    def getElement(self, tp, i):
        return self._post('/connectors/element/' + tp + '.php', data={
            'action': 'get',
            'id': i,
            'HTTP_MODAUTH': self.modauth
        })['object']

    def updateElement(self, tp, i, data):
        data['action'] = 'update'
        data['id'] = i
        data['HTTP_MODAUTH'] = self.modauth
        return self._post('/connectors/element/' + tp + '.php',
            data=data)['object']

    def createElement(self, tp, data):
        data['action'] = 'create'
        data['HTTP_MODAUTH'] = self.modauth
        return self._post('/connectors/element/' + tp + '.php',
            data=data)['object']
