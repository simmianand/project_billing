# -*- coding: utf-8 -*-
"""
    setup.py

    This file contain the setup for the projectbilling module

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from setuptools import setup
import re
import os
import ConfigParser

# pylint: disable-msg=C0103


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

config = ConfigParser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = []
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        requires.append('trytond_%s >= %s.%s, < %s.%s' %
                (dep, major_version, minor_version, major_version,
                minor_version + 1)
        )
requires.append('trytond >= %s.%s, < %s.%s' %
        (major_version, minor_version, major_version, minor_version + 1))

setup(name='trytond_projectbilling',
    version=info.get('version', '0.0.1'),
    description='Tryton projectbilling module',
    long_description=read('README.md'),
    author='Openlabs',
    url='http://www.openlabs.co.in/',
    download_url="http://downloads.tryton.org/" + \
        info.get('version', '0.0.1').rsplit('.', 1)[0] + '/',
    package_dir={'trytond.modules.projectbilling': '.'},
    packages=[
        'trytond.modules.projectbilling',
        ],
    package_data={
        'trytond.modules.projectbilling': info.get('xml', []) \
            + ['tryton.cfg', ],
        },
    classifiers=[
        'Development Status :: 1 - Production/Beta',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        ],
    license='GPL-3',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    projectbilling = trytond.modules.projectbilling
    """,
    )

# pylint: enable-msg=C0103
