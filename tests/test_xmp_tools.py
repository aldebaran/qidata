# Third-party libraries
import pytest

# Local modules
from qidata import _mixin as xmp_tools

def test_unicode_conversion():

	with pytest.raises(TypeError):
		xmp_tools._unicodeListToBuiltInList(())

	data = ["1"]
	xmp_tools._unicodeListToBuiltInList(data)
	assert(data == [1])

	data = ["1.0", "1"]
	xmp_tools._unicodeListToBuiltInList(data)
	assert(data == [1.0, 1])

	data = ["a",["1","2.0"]]
	xmp_tools._unicodeListToBuiltInList(data)
	assert(data == ["a", [1, 2.0]])

	with pytest.raises(TypeError):
		xmp_tools._unicodeToBuiltInType([])