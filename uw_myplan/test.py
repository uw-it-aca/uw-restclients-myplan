# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# This is just a test runner for coverage
import os
from os.path import abspath, dirname

from commonconf.backends import use_configparser_backend

if __name__ == '__main__':
    path = abspath(os.path.join(dirname(__file__),
                                "..", "conf", "test.conf"))
    use_configparser_backend(path, 'MyPlan')

    from nose2 import discover
    discover()
