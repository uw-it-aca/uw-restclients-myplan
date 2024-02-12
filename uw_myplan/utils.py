# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from commonconf import override_settings

fdao_myplan_override = override_settings(
    RESTCLIENTS_MYPLAN_DAO_CLASS='Mock')
fdao_myplan_auth_override = override_settings(
    RESTCLIENTS_MYPLAN_AUTH_DAO_CLASS='Mock')
