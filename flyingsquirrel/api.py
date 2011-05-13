#
# See COPYING for copyright and licensing.
#

import urllib

from .utils import json_request


class API(object):
    def __init__(self, service_url):
        self.base_url = service_url.strip('/') + '/endpoints/'

    def get_endpoint(self, endpoint_name):
        url = self.base_url + urllib.quote(endpoint_name)
        return json_request('GET', url).body

    def create_endpoint(self, endpoint_name, definition=None):
        if definition is None:
            definition = {}
        url = self.base_url + urllib.quote(endpoint_name)
        return json_request('PUT', url, {'definition': definition}).body

    def delete_endpoint(self, endpoint_name):
        url = self.base_url + urllib.quote(endpoint_name)
        json_request('DELETE', url)
        return True

    def list_endpoints(self):
        url = self.base_url
        return json_request('GET', url).body

    def generate_ticket(self, endpoint_name, identity, timeout=None):
        url = self.base_url + urllib.quote(endpoint_name) + '/tickets'
        req = {'identity': identity}
        if timeout is not None:
            req['timeout'] = timeout
        return json_request('POST', url, req).body['ticket']
