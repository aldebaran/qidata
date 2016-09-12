#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

setup(
    name='qidata',
    version=open(os.path.join(CONTAINING_DIRECTORY,"qidata/VERSION")).read().split()[0],
    author='Louis-Kenzo Cahier <lkcahier@aldebaran.com>, Surya Ambrose <sambrose@aldebaran.com>',
    author_email='sambrose@aldebaran.com',
    packages=find_packages("."),
    package_data={"qidata":["VERSION"]},
    scripts=['bin/qidata'],
    url='.',
    license='LICENSE.txt',
    description='Dataset management CLI',
    long_description=open(os.path.join(CONTAINING_DIRECTORY,'README.md')).read(),
    test_suite="tests",
    install_requires=[
        "enum34 >= 1.0.4",
        "xmp >= 0.1",
        "argcomplete >= 1.1.0"
    ]
)
