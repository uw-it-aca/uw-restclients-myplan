# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with MyPlan.
https://wiki.cac.washington.edu/display/MyPlan/Plan+Resource+v1
"""

import json
import logging

from restclients_core.exceptions import DataFailureException

from uw_myplan.dao import MyPlan_DAO
from uw_myplan.models import MyPlan, MyPlanCourse, MyPlanCourseSection, MyPlanTerm

logger = logging.getLogger(__name__)


class Plan:
    """Interface for interacting with the MyPlan Web Service.
    """

    def __init__(self, actas=None):
        self.dao = MyPlan_DAO()

    def _get_plan_url(self, regid, year, quarter, terms):
        return f"/plan/v1/{year},{quarter},{terms},{regid}"

    def _get_resource(self, url, clear_cached_token=False):
        if clear_cached_token:
            self.dao.clear_access_token()

        return self.dao.getURL(url)

    def get_plan(self, regid, year, quarter, terms=4):
        url = self._get_plan_url(regid, year, quarter, terms)

        response = self._get_resource(url)

        if response.status == 200:
            return self._process_data(json.loads(response.data))

        if response.status == 401 or response.status == 403:
            # clear cached access token, retry once
            response = self._get_resource(url, clear_cached_token=True)
            if response.status == 200:
                return self._process_data(json.loads(response.data))

        raise DataFailureException(url, response.status, str(response.data))

    def _process_data(self, jdata):
        plan = MyPlan()
        for term_data in jdata:
            term = MyPlanTerm()
            term.year = term_data["Term"]["Year"]
            term.quarter = term_data["Term"]["Quarter"]
            term.reg_open = term_data["Term"].get("OpenForRegistration")

            term.complete_pre_reg = term_data.get("PreRegistrationComplete")
            term.course_search_href = term_data.get("CourseSearchHref")
            term.degree_audit_href = term_data.get("DegreeAuditHref")
            term.myplan_href = term_data.get("MyPlanHref")

            term.myplan_audit_href = term_data.get("PlanAuditHref")
            term.registration_href = term_data.get("RegistrationHref")
            term.registered_courses_count = int(
                term_data.get("RegisteredCoursesCount", 0))
            term.registered_sections_count = int(
                term_data.get("RegisteredSectionsCount", 0))

            for course_data in term_data["Courses"]:
                course = MyPlanCourse()
                course.curriculum_abbr = course_data["CurriculumAbbreviation"]
                course.course_number = course_data["CourseNumber"]

                is_available = course_data["RegistrationAvailable"]
                course.registrations_available = is_available

                for section_data in course_data["Sections"]:
                    section = MyPlanCourseSection()
                    section.section_id = section_data["SectionId"]
                    course.sections.append(section)

                term.courses.append(course)
            plan.terms.append(term)
        return plan
