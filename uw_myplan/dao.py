# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import os
from os.path import abspath, dirname

from restclients_core.dao import DAO
from restclients_core.exceptions import DataFailureException

logger = logging.getLogger(__name__)


class MyPlan_Auth_DAO(DAO):
    """ DAO for MyPlan OAuth2 Authentication
    """
    myplan_access_token_url = "/oauth2/token"

    def service_name(self):
        return "myplan_auth"

    def _is_cacheable(self, method, url, headers, body=None):
        return True

    def _custom_headers(self, method, url, headers, body):
        """ Add custom headers for SPS Contacts Auth requests
        """
        if not headers:
            headers = {}

        secret = self.get_service_setting("SECRET")

        headers["Authorization"] = f"Basic {secret}"
        headers["Content-type"] = "application/x-www-form-urlencoded"

        return headers

    def clear_token_from_cache(self):
        self.clear_cached_response(self.myplan_access_token_url)

    def get_auth_token(self):
        """ Get an OAuth2 access token from MyPlan Auth
        """
        response = self.postURL(
            self.myplan_access_token_url,
            body="grant_type=client_credentials",
        )

        if response.status == 200:
            data = json.loads(response.data)
            return data.get("access_token", "")

        # Something bad happened
        logger.error({
            "url": self.myplan_access_token_url,
            "status": response.status,
            "data": response.data,
        })

        raise DataFailureException(
            self.myplan_access_token_url, response.status, response.data)

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def _edit_mock_response(self, method, url, headers, body, response):
        if response.status == 404 and method != "GET":
            alternative_url = f"{url}.{method}"
            backend = self.get_implementation()
            new_resp = backend.load(method, alternative_url, headers, body)
            response.status = new_resp.status
            response.data = new_resp.data
            logger.debug({
                "url": alternative_url,
                "status": response.status,
                "data": response.data
            })


class MyPlan_DAO(DAO):
    """ DAO for MyPlan API requests
    """
    def __init__(self):
        self.auth_dao = MyPlan_Auth_DAO()
        super().__init__()

    def service_name(self):
        return "myplan"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def _custom_headers(self, method, url, headers, body):
        if not headers:
            headers = {}

        token = self.auth_dao.get_auth_token()

        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/json"
        return headers

    def clear_access_token(self):
        self.auth_dao.clear_token_from_cache()
