def for_each(ls, func):
	if type(ls) != type(list()):
		return None
	return [func(l) for l in ls]
