#!/usr/bin/env python
# encoding: UTF-8

from distutils.core import setup

setup(
    name = 'mail1',
    version = 'VERSION',
    author = 'Michel Casabianca',
    author_email = 'casa@sweetohm.net',
    packages = ['mail1'],
    url = 'http://pypi.python.org/pypi/mail1/',
    license = 'Apache Software License',
    description = 'mail1 is an API to send emails in a single call',
    long_description=open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'mail1 = mail1:run',
        ],
    },
)
