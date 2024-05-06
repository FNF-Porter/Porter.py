"""
A class full of tools needed for chart conversion.
"""

from src import Constants

def character(name:str) -> str:
	"""
	Some characters might have changed names in the Base Game,
	this will help you convert their names.

	Args:
		name (str): Name of the character.
	"""

	return Constants.CHARACTERS.get(name, name)

def stage(name:str) -> str:
	"""
	Some stages might have changed names in the Base Game,
	this will help you convert their names.

	Args:
		name (str): Name of the stage.
	"""

	return Constants.STAGES.get(name, name)

def timeChange(timeStamp:float, bpm:float, timeSignatureNum:int, timeSignatureDen:int, beatTime:int, beatTuplets:list) -> dict:
	"""
	Function created for faster creation of song time changes.
	"""
	return {
		"t": timeStamp,
		"b": beatTime,
		"bpm": bpm,
		"n": timeSignatureNum,
		"d": timeSignatureDen,
		"bt": beatTuplets
	}

def note(time:str, data:int, length:float) -> dict:
	"""
	Function created for faster creation of note data.
	"""
	return {
		"t": time,
		"d": data,
		"l": length
	}