# -*- coding:utf-8 -*-
import os

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('README.md') as fh:
    README = fh.read()

setup(
    name='kafka-tracker',
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='',
    long_description=README,
    # url='',
    setup_requires=['setuptools_scm==3.5.0'],
)
