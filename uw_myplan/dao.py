# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from os.path import abspath, dirname
from restclients_core.dao import DAO


class MyPlan_DAO(DAO):
    def service_name(self):
        return 'myplan'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]
