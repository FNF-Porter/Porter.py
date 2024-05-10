def toString(val:any) -> str:
	"""
	Converts any value to a string
	"""

	instance = type(val)
	if instance == str:
		return val
	val = str(val)
	if instance == bool:
		return val.lower()
	return val