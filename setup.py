#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

try:
    from utils import get_version_from_tag
    __version__ = get_version_from_tag()
    open(os.path.join(CONTAINING_DIRECTORY,"qidata/VERSION"), "w").write(__version__)
except ImportError:
    __version__=open(os.path.join(CONTAINING_DIRECTORY,"qidata/VERSION")).read().split()[0]

package_list = find_packages(where=os.path.join(CONTAINING_DIRECTORY))

setup(
    name='qidata',
    version=__version__,
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
        "setuptools >= 35.0.0",
        "enum34 >= 1.0.4",
        "strong_typing >= 0.1.4",
        "xmp >= 0.3",
        "qidata_devices >= 0.0.3",
    ],
    package_data={"qidata":["VERSION"]},
    scripts=['bin/qidata'],
    entry_points={
        'qidata.metadata.definition': [
            'Face = qidata._metadata_objects.face:Face',
            'Object = qidata._metadata_objects.object:Object',
            'Person = qidata._metadata_objects.person:Person',
            'Speech = qidata._metadata_objects.speech:Speech',
        ],
    }
)