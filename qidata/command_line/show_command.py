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

# Standard libraries
import os
import sys

# Third-party libraries
import argparse
try:
	import argcomplete
	has_argcomplete = True
except ImportError:
	has_argcomplete = False

# Local modules
import qidata
from qidata import qidataset

DESCRIPTION = "Shows information about a QiData element"

class ShowCommand:

	@staticmethod
	def show(args):
		throwIfAbsent(args.path)
		if qidataset.isDataset(args.path):
			with qidataset.QiDataSet(args.path) as p:
				return str(p)
		elif os.path.isdir(args.path):
			sys.exit(args.path+" isn't a valid QiDataSet")

		elif qidata.isSupported(args.path):
			with qidata.open(args.path) as p:
				return str(p)

		else:
			sys.exit(args.path+" is not supported")

# ───────
# Helpers

def throwIfAbsent(path):
	if not os.path.exists(path):
		sys.exit(path+" doesn't exist")

# ──────
# Parser

def make_command_parser(parent_parser=argparse.ArgumentParser(description=DESCRIPTION)):
	path_argument = parent_parser.add_argument("path", help="what to examine")
	if has_argcomplete: path_argument.completer = argcomplete.completers.FilesCompleter()
	parent_parser.set_defaults(func=ShowCommand.show)
	return parent_parser
