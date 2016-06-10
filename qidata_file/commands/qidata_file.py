# -*- coding: utf-8 -*-

# Standard Library
import os.path

# Qidata
from ..qidatafile import QiDataFile

class QiDataFilesCommand:

	@staticmethod
	def show(args):
		throwIfAbsent(args.file)
		input_file_path = args.file
		qidata_file = QiDataFile(input_file_path)
		with qidata_file as p:
			if p.metadata.children:
				print p.metadata
			else:
				print "No QiDataObjects"

# ───────
# Helpers

def throwIfAbsent(file_path):
	if not os.path.isfile(file_path):
		import sys
		sys.exit("File "+file_path+" doesn't exist")