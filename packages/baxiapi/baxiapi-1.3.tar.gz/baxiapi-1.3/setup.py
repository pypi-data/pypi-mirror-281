import os
from setuptools import setup, find_packages

setup(
    name='baxiapi',
    version='1.3',
    packages=["api"],
    install_requires=["requests"],
    author="Red_Wolf2467",
    author_email="support@pyropixle.com",
    description="Allows you to interact with our Baxi API."
)