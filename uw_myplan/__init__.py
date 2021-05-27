# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with MyPlan.
https://wiki.cac.washington.edu/display/MyPlan/Plan+Resource+v1
"""

from uw_myplan.dao import MyPlan_DAO
from restclients_core.exceptions import DataFailureException
from uw_myplan.models import (
    MyPlan, MyPlanTerm, MyPlanCourse, MyPlanCourseSection)
import json


def get_plan(regid, year, quarter, terms=4):
    dao = MyPlan_DAO()
    url = get_plan_url(regid, year, quarter, terms)

    response = dao.getURL(url, {"Accept": "application/json"})
    if response.status != 200:
        raise DataFailureException(url, response.status, str(response.data))

    data = json.loads(response.data)

    plan = MyPlan()
    for term_data in data:
        term = MyPlanTerm()
        term.year = term_data["Term"]["Year"]
        term.quarter = term_data["Term"]["Quarter"]

        term.course_search_href = term_data["CourseSearchHref"]
        term.degree_audit_href = term_data["DegreeAuditHref"]
        term.myplan_href = term_data["MyPlanHref"]
        term.registration_href = term_data["RegistrationHref"]
        term.registered_courses_count = int(
            term_data["RegisteredCoursesCount"])
        term.registered_sections_count = int(
            term_data["RegisteredSectionsCount"])

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


def get_plan_url(regid, year, quarter, terms=4):
    return "/student/api/plan/v1/{year},{quarter},{terms},{uwregid}".format(
        year=year, quarter=quarter, terms=terms, uwregid=regid)
