# uw-restclients-myplan

[![Build Status](https://github.com/uw-it-aca/uw-restclients-myplan/workflows/tests/badge.svg?branch=main)](https://github.com/uw-it-aca/uw-restclients-myplan/actions)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/uw-restclients-myplan/badge.svg?branch=main)](https://coveralls.io/r/uw-it-aca/uw-restclients-myplan?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/uw-restclients-myplan.svg)](https://pypi.python.org/pypi/uw-restclients-myplan)
![Python versions](https://img.shields.io/badge/python-3.10-blue.svg)


Installation:

    pip install UW-RestClients-MyPlan

To use this client, you'll need these settings in your application or script:

    # Specifies whether requests should use live or mocked resources,
    # acceptable values are 'Live' or 'Mock' (default)
    RESTCLIENTS_MYPLAN_DAO_CLASS='Live'
    RESTCLIENTS_MYPLAN_AUTH_DAO_CLASS='Live'
    RESTCLIENTS_MYPLAN_AUTH_SECRET=''
    RESTCLIENTS_MYPLAN_AUTH_HOST=''
