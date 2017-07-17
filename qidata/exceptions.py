
class ReadOnlyException(Exception):pass

def throwIfReadOnly(f):
	def wraps(*args):
		self=args[0]
		if self.read_only:
			raise ReadOnlyException("This method cannot be used in read-only")
		return f(*args)
	return wraps