#
# See COPYING for copyright and licensing.
#

import base64
import urllib2
import re
import json

from . import exceptions


class JsonResponse(object):
    pass

def json_request(method, url, body=None):
    # urllib2 doesn't understand user/pass in the url
    scheme, _, username, password, rest = \
        re.match("^([^:]*://)(([^:]*):([^@]*)@)?(.*)", url).groups()
    stripped_url = scheme + rest

    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    if username is not None and password is not None:
        password_mgr.add_password(None, stripped_url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    opener = urllib2.build_opener(handler)

    request = urllib2.Request(stripped_url,
                              headers={"Content-type": "application/json"})
    if body is not None:
        request.add_data(json.dumps(body)),
    request.get_method = lambda : method

    try:
        response = opener.open(request)
    except urllib2.HTTPError as e:
        raise exceptions.HttpError(url, e.getcode(), e.read())

    res = JsonResponse()
    res.status = response.getcode()
    res.body = response.read()
    res.headers = dict(response.info().items())

    if res.status in (200, 204):
        if res.headers['content-type'] == "application/json" and res.body:
            res.body = json.loads(res.body)
    else:
        raise exceptions.HttpError(url, res.status, res.body)
    return res
