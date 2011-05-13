#
# See COPYING for copyright and licensing.
#

import os
import random
import string
import unittest

import flyingsquirrel

rand_str = lambda: ''.join(random.choice(string.letters) for i in xrange(8))


SERVICE_URL=os.environ.get('SERVICE_URL', 'http://guest:guest@localhost:55672/socks-api/default')

class TestAPI(unittest.TestCase):
    def test_list(self):
        c = flyingsquirrel.API(SERVICE_URL)
        self.assertIsInstance(c.list_endpoints(), list)

    def test_basic(self):
        # Create endpoint, check if it appears in the list, get, delete.
        c = flyingsquirrel.API(SERVICE_URL)
        endpoint_name = rand_str()

        e = c.create_endpoint(endpoint_name, {})
        self.assertEqual(e['endpoint_name'], endpoint_name)

        self.assertTrue(filter(lambda i:e['endpoint_name'] == endpoint_name,
                               c.list_endpoints()))

        e = c.get_endpoint(endpoint_name)
        self.assertEqual(e['endpoint_name'], endpoint_name)

        self.assertTrue(c.delete_endpoint(endpoint_name))

    def test_errors(self):
        c = flyingsquirrel.API(SERVICE_URL)
        endpoint_name = rand_str()

        with self.assertRaises(flyingsquirrel.HttpError) as e:
            c.get_endpoint(endpoint_name)
        self.assertEquals(e.exception[1], 404)

        with self.assertRaises(flyingsquirrel.HttpError) as e:
            c.delete_endpoint(endpoint_name)
        self.assertEquals(e.exception[1], 404)

    def test_ticket(self):
        c = flyingsquirrel.API(SERVICE_URL)
        endpoint_name = rand_str()

        e1 = c.create_endpoint(endpoint_name, {})
        self.assertEqual(e1['endpoint_name'], endpoint_name)
        e2 = c.get_endpoint(endpoint_name)
        self.assertEqual(e1, e2)

        t = c.generate_ticket(endpoint_name, 'guest')
        self.assertIsInstance(t, unicode)
        self.assertTrue(len(t))

        self.assertTrue(c.delete_endpoint(endpoint_name))


if __name__ == '__main__':
    unittest.main()

