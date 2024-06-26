#!/usr/bin/env python3
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

data = {
    'name': 'djradicale',
    'version': '0.0.16',
    'author': 'Kyoken',
    'author_email': 'kyoken@kyoken.ninja',
    'description': (
        'Radicale is a free and open-source CalDAV and CardDAV server.'
        'DjRadicale is an Django Application for integration Radicale '
        'with a Django.'),
    'license': 'GPLv3',
    'keywords': 'django radicale carddav caldav',
    'url': 'https://github.com/kyokenn/djradicale',
    'packages': [
        'djradicale',
        'djradicale.migrations',
        'djradicale.tests',
    ],
    'long_description': '',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Framework :: Django',
    ],
    'install_requires': [
        'Django >= 4.0.1',
        'Radicale >= 3.1.2',
    ],
}

setup(**data)
