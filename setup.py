#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

package_list = find_packages(where=CONTAINING_DIRECTORY)

setup(
    name='qidata',
    version=open(os.path.join(CONTAINING_DIRECTORY,"qidata/VERSION")).read().split()[0],
    description='Metadata annotation tool',
    long_description=open(os.path.join(CONTAINING_DIRECTORY,'README.rst')).read(),
    url='https://gitlab.aldebaran.lan/qidata/qidata',
    author='Surya Ambrose <sambrose@aldebaran.com>, Louis-Kenzo Cahier <lkcahier@aldebaran.com>',
    author_email='sambrose@aldebaran.com',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='metadata annotation tagging',
    packages=package_list,
    install_requires=[
        "enum34 >= 1.0.4",
        "strong_typing >= 0.1",
        "xmp >= 0.1",
    ],
    package_data={"qidata":["VERSION", "../README.rst"]},
    scripts=['bin/qidata'],
)
