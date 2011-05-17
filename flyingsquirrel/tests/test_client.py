#
# See COPYING for copyright and licensing.
#

import os
import random
import string
import sys
import threading
import BaseHTTPServer
import Queue
try:
    # For python2.6 we need unittest backported from 2.7.
    import unittest2 as unittest
except ImportError:
    import unittest


import flyingsquirrel
from .common import rand_str, SERVICE_URL

REQUESTS = None


class TestHttpServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        if body:
            REQUESTS.put((body, self.headers))
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

class ServerThread(threading.Thread):
    def run(self):
        print " [.] Running server on %s" % (self.port,)
        server = BaseHTTPServer.HTTPServer(('', self.port), TestHttpServer)
        server.timeout = 0.1
        while not self.stop.isSet():
            server.handle_request()



def test_with_endpoint(endpoint_definition, identity):
    def a(f):
        def wrapper(self):
            self.endpoint_name = rand_str()

            self.c = flyingsquirrel.API(SERVICE_URL)
            self.e = self.c.create_endpoint(self.endpoint_name,
                                            endpoint_definition)
            self.assertEqual(self.e['endpoint_name'], self.endpoint_name)

            self.t = self.c.generate_ticket(self.endpoint_name, identity)
            self.assertIsInstance(self.t, unicode)
            self.assertTrue(len(self.t))

            r = f(self)

            self.assertTrue(self.c.delete_endpoint(self.endpoint_name))
            return r
        return wrapper
    return a

class WebHooksClientTestsBase(unittest.TestCase):
    port = 8125

    def setUp(self):
        global REQUESTS
        REQUESTS = Queue.Queue()
        self.thread = ServerThread()
        self.thread.stop = threading.Event()
        self.thread.port = self.port
        self.thread.start()

    def tearDown(self):
        print " [.] Waiting for thread to teardown"
        self.thread.stop.set()
        self.thread.join()



class TestWebHooksClient(WebHooksClientTestsBase):
    @test_with_endpoint({'send': ['pub', 'echo'],
                         'recv': ['sub', 'echo']}, 'guest')
    def test_pub_sub(self):
        self.url = 'http://localhost:%i/' % (self.port,)

        conn = flyingsquirrel.WebHooksClient(self.e['protocols']['webhooks'],
                                             self.t,
                                             self.url)
        r=[None]
        def cb(data, **kwargs):
            r[0]=data
        conn.subscribe('recv', cb)

        conn.publish('send', 'test')

        body, headers = REQUESTS.get()
        self.assertTrue(body)
        conn.deliver_message(body, headers)
        # Make sure the callback was run.
        self.assertEqual(r[0], 'test')
        conn.disconnect()


    @test_with_endpoint({'req': ['req', 'x-reqrep'],
                         'rep': ['rep', 'x-reqrep']}, 'guest')
    def test_req_rep(self):
        self.url = 'http://localhost:%i/' % (self.port,)

        conn = flyingsquirrel.WebHooksClient(self.e['protocols']['webhooks'],
                                             self.t,
                                             self.url)
        def worker(msg, send_answer, **kwargs):
            print send_answer('r_' + msg)
        conn.serve('rep', worker)

        answers = []
        def cb(answer, **kwargs):
            answers.append(answer)
        conn.request('req', 'a', cb)

        body, headers = REQUESTS.get()
        conn.deliver_message(body, headers)
        body, headers = REQUESTS.get()
        conn.deliver_message(body, headers)

        self.assertEqual(answers, ['r_a'])
        conn.disconnect()

if __name__ == '__main__':
    unittest.main()
