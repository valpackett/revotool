import re
import requests
from requests.auth import HTTPBasicAuth
from posixpath import join


RE_AUTH = re.compile('.*auth: ?"([^"]+)".*', re.DOTALL)
RE_DOMAIN = re.compile('https?://[^/]+')


class MODXException(Exception):
    pass


class MODXBasicAuthException(MODXException):
    pass


class MODXClient(object):

    def __init__(self, host, username, password, basic_username=None,
            basic_password=None):
        if host[0] == 'h':
            self.host = host
        else:
            self.host = 'http://' + host
        self.http = requests.Session()
        if basic_username and basic_password:
            self.http.auth = HTTPBasicAuth(basic_username, basic_password)
        url = join(self.host, 'manager/')
        self.http.get(url)
        res = self.http.post(url, data={
            'login_context': 'mgr',
            'modahsh': '',
            'returnUrl': RE_DOMAIN.sub('', url),
            'username': username,
            'password': password,
            'login': '1'
        }, headers={
            'Referer': url
        })
        if res.status_code == 401:
            if not (basic_username and basic_password):
                raise MODXBasicAuthException("HTTP Basic auth required")
            else:
                raise MODXBasicAuthException("Wrong HTTP Basic auth")
        try:
            self.modauth = RE_AUTH.match(res.text).groups()[0]
        except AttributeError:
            raise MODXException("Wrong password OR something's broken")

    def _post(self, url, params={}, data={}):
        res = self.http.post(join(self.host, url),
            params=params, data=data).json()
        if isinstance(res, dict):
            if not res['success']:
                raise MODXException(str(res['data']))
        return res

    def _postElement(self, tp, data):
        data['HTTP_MODAUTH'] = self.modauth
        return self._post('connectors/element/' + tp + '.php',
            data=data)['object']

    def getElements(self, tp, node=None):
        if not node:
            node = 'n_type_' + tp
        return self._post('connectors/element/index.php',
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
        return self._post('connectors/element/' + tp + '.php', data={
            'action': 'get',
            'id': i,
            'HTTP_MODAUTH': self.modauth
        })['object']

    def updateElement(self, tp, i, data={}):
        data['action'] = 'update'
        data['id'] = i
        return self._postElement(tp, data)

    def createElement(self, tp, data={}):
        data['action'] = 'create'
        return self._postElement(tp, data)

    def removeElement(self, tp, i, data={}):
        data['action'] = 'remove'
        data['id'] = i
        return self._postElement(tp, data)
