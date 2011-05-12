import urllib

from .utils import json_request
from . import exceptions


class Client(object):
    def __init__(self, base_url):
        self.base_url = base_url.strip('/')

    def create_endpoint(self, endpoint_name, definition={}):
        url = self.base_url + '/endpoints/' \
            + urllib.quote(endpoint_name)
        res = json_request('PUT', url, {'definition': definition})
        return res.body

    def delete_endpoint(self, endpoint_name):
        url = self.base_url + '/endpoints/' \
            + urllib.quote(endpoint_name)
        res = json_request('DELETE', url)
        return True

    def list_endpoints(self):
        url = self.base_url + '/endpoints'
        res = json_request('GET', url)
        return res.body

    def generate_ticket(self, endpoint_name, identity, timeout=None):
        url = self.base_url + '/endpoints/' \
            + urllib.quote(endpoint_name) + '/tickets'
        req = {'identity': identity}
        if timeout is not None:
            req['timeout'] = timeout
        res = json_request('POST', url, req)
        return res.body['ticket']


