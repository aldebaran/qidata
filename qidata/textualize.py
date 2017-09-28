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

# ─────────────────────
# Formatting parameters

INDENT_SIZE = 3
AFTER_MID_INDENT = u'│' + ' ' * (INDENT_SIZE-1)
AFTER_LAST_INDENT = ' ' * (INDENT_SIZE)
TREE_INDENT = u'─'*(INDENT_SIZE-2) + " "
TREE_MID_INDENT  = u"├" + TREE_INDENT
TREE_LAST_INDENT = u"└" + TREE_INDENT


def textualize_annotations(annotations_to_display):
	res_str = ""
	if len(annotations_to_display) > 0:
		for i in range(len(annotations_to_display)):
			annotation_str = "\n"
			if i != len(annotations_to_display)-1:
				annotation_str += TREE_MID_INDENT
				indent_level = AFTER_MID_INDENT
			else:
				annotation_str += TREE_LAST_INDENT
				indent_level = AFTER_LAST_INDENT
			annotation_str += "%d: "%i
			annotation_str += " (Location: " + unicode(annotations_to_display[i][1]) + "):"
			annotation_str += unicode(annotations_to_display[i][0]).replace("\n","\n"+(indent_level))
			res_str += annotation_str
	else:
		res_str += "\n" + TREE_LAST_INDENT + "[]"
	return res_str

def textualize_metadata(metadata_to_display):
	res_str = ""
	for metadata_type in metadata_to_display:
		key = metadata_type
		metadata_type_str = "\n"
		if metadata_type != metadata_to_display.keys()[-1]:
			metadata_type_str += TREE_MID_INDENT + metadata_type
			indent_level = AFTER_MID_INDENT
		else:
			metadata_type_str += TREE_LAST_INDENT + metadata_type
			indent_level = AFTER_LAST_INDENT
		res_str += metadata_type_str
		res_str += textualize_annotations(metadata_to_display[metadata_type]).replace("\n","\n"+(indent_level))
	return res_str