#
# See COPYING for copyright and licensing.
#

from setuptools import setup

# Some filesystems don't support hard links. Use the power of
# monkeypatching to overcome the problem.
import os, shutil
os.link = shutil.copy


long_description = """\
Flyingsquirrel is a Python library for use with the Flying Squirrel
service.
"""

setup(name = 'flyingsquirrel',
      version = file('VERSION').read().strip(),
      description = 'Flying Squirrel Client Library',
      long_description = long_description,
      author = 'RabbitMQ Team',
      author_email = 'info@rabbitmq.com',
      packages = ['flyingsquirrel'],
      test_suite = 'flyingsquirrel.tests',
      license = 'MPL v1.1',
      platforms = ['any'],
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
        'Operating System :: OS Independent',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        ],
      zip_safe = True
      )
