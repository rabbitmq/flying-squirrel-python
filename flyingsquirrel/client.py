#
# See COPYING for copyright and licensing.
#
import json
import random
import string
from .utils import json_request


rand_str=lambda: ''.join(random.choice(string.letters) for i in xrange(8))


class WebHooksClient(object):
    def __init__(self, protocol_url, ticket, callback_url, key=None):
        self.key = key or rand_str()
        r = json_request('POST', protocol_url, {'connect': ticket,
                                                'callback_url': callback_url,
                                                'key': self.key})
        assert r.status == 201
        self.location = r.headers['location']
        self.channels = {}

    def disconnect(self):
        json_request('DELETE', self.location, headers={'X-hooks-key': self.key})

    def deliver_message(self, body, headers):
        if headers['x-hooks-key'] != self.key:
            # Someone is calling us with wrong key. Let's tell him to
            # go away and not bother us again.
            return 404
        if not body:
            # Keepalive request
            return 200
        msg = json.loads(body)
        channel = msg['channel']
        if channel in self.channels:
            self.channels[ channel ](msg['body'], channel=channel, msgobj=msg)
        elif 'error-code' in msg:
            # TODO: Use proper exception
            raise Exception(msg['error-code'], msg)
        else:
            # undelivered
            pass
        return 200


    def publish(self, channel, body, msgobj=None):
        m = {}
        if msgobj: m.update(msgobj)
        m.update({'channel': channel, 'body': body})
        self._send(m)

    def subscribe(self, channel, callback):
        self.channels[channel] = callback


    def request(self, channel, question, callback):
        def cb(answer, **kwargs):
            del self.channels[channel]
            callback(answer, **kwargs)
        self.subscribe(channel, cb)
        self.publish(channel, question)

    def serve(self, channel, callback):
        def cb(msg, channel=None, msgobj=None, **kwargs):
            def an(answer):
                return self._send({'channel': channel,
                                   'reply-to':msgobj['reply-to'],
                                   'body': answer})
            callback(msg, an, **kwargs)
        self.subscribe(channel, cb)


    def _send(self, msg):
        return json_request('POST', self.location, msg,
                            headers={'X-hooks-key': self.key})
