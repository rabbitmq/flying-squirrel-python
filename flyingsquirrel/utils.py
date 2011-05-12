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
    response = opener.open(request)

    response_data = response.read()

    if response.getcode() == 200 and response_data:
        response_data = json.loads(response_data)
    else:
        raise exceptions.HttpError("Error on: %s %s -> %s %s" %
                                   (method, url, response.getcode(), response_data))
    res = JsonResponse()
    res.status = response.getcode()
    res.body = response_data
    res.headers = dict(response.info().items())

    if res.status not in (200,):
        raise exceptions.HttpError("%r --> %r %r" %
                                   (url, res.status, res.body))
    return res
