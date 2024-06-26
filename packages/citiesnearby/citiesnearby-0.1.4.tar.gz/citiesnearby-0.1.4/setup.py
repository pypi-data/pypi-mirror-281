from setuptools import setup, find_packages

setup(
    name="citiesnearby",
    version="0.1.4",
    packages=find_packages(),
    requires=['requests'],
    description='Library to use CitiesNearby API.',
    long_description='See the documentation for the API and Library here: https://marz1ks-organization.gitbook.io/citiesnearby-api/'
)