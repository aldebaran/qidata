#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
    license='BSD-3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='metadata annotation tagging',
    packages=package_list,
    install_requires=[
        "opencv-python >= 3.0",
        "setuptools >= 35.0.0",
        "enum34 >= 1.0.4",
        "strong_typing >= 0.2.2",
        "xmp >= 0.3",
        "qidata_devices >= 0.0.3",
        "image.py >= 0.4.0",
    ],
    package_data={"qidata":["VERSION"]},
    entry_points={
        'qidata.metadata.definition': [
            'Face = qidata._metadata_objects.face:Face',
            'Object = qidata._metadata_objects.object:Object',
            'Person = qidata._metadata_objects.person:Person',
            'Speech = qidata._metadata_objects.speech:Speech',
        ],
        'qidata.commands': [
            'show = qidata.command_line.show_command',
        ],
        'console_scripts': [
            'qidata = qidata.__main__:main'
        ]
    }
)