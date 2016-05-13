#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup
import os

CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

setup(
    name='qidata_file',
    version=open(os.path.join(CONTAINING_DIRECTORY,"qidata_file/VERSION")).read().split()[0],
    author='Louis-Kenzo Cahier',
    author_email='lkcahier@aldebaran.com',
    packages=['qidata_file', 'qidata_file.qiq'],
    package_data={"qidata_file":["VERSION"]},
    url='.',
    license='LICENSE.txt',
    description='Uses XMP library to store data_objects instances in files metadata fields.',
    long_description=open(os.path.join(CONTAINING_DIRECTORY,'README.md')).read(),
    test_suite="tests",
    install_requires=[
        "xmp >= 0.1",
        "qidata_objects >= 0.1",
        "argcomplete >= 1.1.0"
    ]
)

