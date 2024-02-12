# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-restclients-myplan>`_.
"""

version_path = 'uw_myplan/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='UW-RestClients-MyPlan',
    version=VERSION,
    packages=['uw_myplan'],
    author="UW-IT T&LS",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'UW-RestClients-Core',
        'mock',
        ],
    license='Apache License, Version 2.0',
    description=('A library for connecting to the UW MyPlan API'),
    long_description=README,
    url="https://github.com/uw-it-aca/uw-restclients-myplan",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
