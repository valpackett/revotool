#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()

requirements = [
    'docopt',
    'requests'
]

setup(
    name='revotool',
    version='0.1.0',
    description='Revotool is a CLI tool for working with MODX Revolution™',
    long_description=readme,
    author='Greg V',
    author_email='floatboth@me.com',
    url='https://github.com/myfreeweb/revotool',
    packages=[
        'revotool',
    ],
    scripts=[
        'scripts/revotool'
    ],
    package_dir={'revotool': 'revotool'},
    include_package_data=True,
    install_requires=requirements,
    license='Apache License 2.0',
    zip_safe=False,
    keywords='revotool',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ]
)
