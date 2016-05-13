#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup
import os

CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

setup(
    name='qidata_objects',
    version=open(os.path.join(CONTAINING_DIRECTORY,"qidata_objects/VERSION")).read().split()[0],
    author='Surya Ambrose',
    author_email='sambrose@aldebaran.com',
    packages=['qidata_objects'],
    package_data={"qidata_objects":["VERSION"]},
    scripts=['bin/qidata_objects'],
    url='.',
    license='LICENSE.txt',
    description='Library containing data objects definition',
    long_description=open(os.path.join(CONTAINING_DIRECTORY,'README.md')).read(),
    install_requires=[]
)

