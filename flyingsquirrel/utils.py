#
# See COPYING for copyright and licensing.
#

import urllib2
import re
import json

from . import exceptions


class JsonResponse(object):
    def __init__(self, status, body, headers):
        self.status = status
        self.body = body
        self.headers = headers

def json_request(method, url, body=None, headers=None):
    # urllib2 doesn't understand user/pass in the url
    scheme, _, username, password, rest = \
        re.match("^([^:]*://)(([^:]*):([^@]*)@)?(.*)", url).groups()
    stripped_url = scheme + rest

    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    if username is not None and password is not None:
        password_mgr.add_password(None, stripped_url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    opener = urllib2.build_opener(handler)

    if headers is None:
        headers = {}
    headers.update({"Content-type": "application/json"})

    request = urllib2.Request(stripped_url, headers=headers)
    if body is not None:
        request.add_data(json.dumps(body))
    request.get_method = lambda : method

    try:
        response = opener.open(request)
    except urllib2.HTTPError as ex:
        raise exceptions.HttpError(method, url, ex.getcode(), ex.read())

    res = JsonResponse(response.getcode(),
                       response.read(),
                       dict(response.info().items()))

    if res.status in (200, 201, 204):
        if res.headers['content-type'] == "application/json" and res.body:
            res.body = json.loads(res.body)
    else:
        raise exceptions.HttpError(url, res.status, res.body)
    return res
