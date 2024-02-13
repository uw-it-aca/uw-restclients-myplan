# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
import mock
from commonconf import override_settings
from restclients_core.exceptions import DataFailureException
from restclients_core.models import MockHTTP
from uw_myplan.dao import MyPlan_Auth_DAO, MyPlan_DAO
from uw_myplan.utils import (
    fdao_myplan_override, fdao_myplan_auth_override)


@fdao_myplan_auth_override
@fdao_myplan_override
class TestMyPlanAuth(TestCase):

    def test_is_cacheable(self):
        auth = MyPlan_Auth_DAO()
        self.assertTrue(auth._is_cacheable("POST", "/", {}, ""))

    def test_get_auth_token(self):
        self.assertIsNotNone(
            MyPlan_Auth_DAO().get_auth_token("test1"))

    @mock.patch.object(MyPlan_Auth_DAO, "postURL")
    def test_get_auth_token_error(self, mock):
        response = MockHTTP()
        response.status = 404
        response.data = "Not Found"
        mock.return_value = response
        self.assertRaises(
            DataFailureException,
            MyPlan_Auth_DAO().get_auth_token, "test1")

    def test_no_auth_header(self):
        headers = MyPlan_DAO()._custom_headers("GET", "/", {}, "")
        self.assertFalse("Authorization" in headers)

    @override_settings(RESTCLIENTS_MYPLAN_AUTH_SECRET="test1")
    @mock.patch.object(MyPlan_Auth_DAO, "get_auth_token")
    def test_auth_header(self, mock_get_auth_token):
        mock_get_auth_token.return_value = "abcdef"
        headers = MyPlan_DAO()._custom_headers("GET", "/", {}, "")
        self.assertTrue("Authorization" in headers)
        self.assertEqual(headers["Authorization"], "abcdef")
