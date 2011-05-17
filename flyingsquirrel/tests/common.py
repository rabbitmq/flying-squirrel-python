#
# See COPYING for copyright and licensing.
#
import random
import string
import os

rand_str=lambda: ''.join(random.choice(string.letters) for i in xrange(8))

SERVICE_URL=os.environ.get('SERVICE_URL',
                           'http://guest:guest@localhost:55670/socks-api/default')
