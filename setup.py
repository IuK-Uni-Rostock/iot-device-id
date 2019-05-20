#!/usr/bin/env python3

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'iot-device-id'
DESCRIPTION = 'Identifies specific IoT devices based on SSDP announcements or DNS requests.'
URL = 'https://git.informatik.uni-rostock.de/iuk/security-projects/software/iot-device-id'
EMAIL = 'johann.bauer@uni-rostock.de'
AUTHOR = 'Johann Bauer'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

here = os.path.abspath(os.path.dirname(__file__))

long_description = open("{}/README.md".format(here)).read()
required = open("{}/requirements.txt".format(here)).readlines()

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=required,
    extras_require={
        'dev': ['pytest-cov', 'coveralls']
    },
    include_package_data=True,
    license='Apache',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)
