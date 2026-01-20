# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "statistics_manager_service"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Statistics Manager Service",
    author_email="vasco.m.campos@inesctec.pt",
    url="",
    keywords=["OpenAPI", "Statistics Manager Service"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['statistics_manager_service=statistics_manager_service.__main__:main']},
    long_description="""\
    This is the Statistics Manager Service OpenAPI definition. The Statistics Manager Service processes energy data in order to provide the user with useful statistics (e.g. energy cost for the day, injection for the month, consumption for the year, CO2 footprint). The interactions here represented are based on this [Canvas](https://gitlab.inesctec.pt/cpes/european-projects/interconnect/hems/hems-documentation/-/blob/master/Microservices/Statistics-Manager-Service.adoc)
    """
)

