"""
A class full of tools needed for mod conversion.
"""

import time
from src import Constants
from re import sub

def getRuntime(start:float) -> float:
	return start - time.time()

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

def note(data:int, length:float, time:str) -> dict:
	"""
	Function created for faster creation of note data.
	"""
	if length == 0 or isinstance(length, str): # String check for more modified Psych Engines
		return {"d": data, "t": time} # This is how the base game charts handle it so...
	return {"d": data, "l": length, "t": time}

def event(event:str, time:float, values:dict) -> dict:
	"""
	Function created for faster creation of events.
	"""
	return {"e": event, "t": time, "v": values}

def focusCamera(time:float, char:bool):
	"""
	Function created for faster creation of camera change events.
	"""
	return event("FocusCamera", time, {"char": "0" if char else "1"})

def coolText(text:str) -> str:
	length = max(30, len(text) + 5)
	length += len(text) % 2

	text = " " * ((length - len(text)) // 2) + text
	return "\n" + "=" * length + f"\n{text}\n" + "=" * length

def formatToSongPath(name:str) -> str:
	invalidChars = r'[~&\\;:<>#]'
	hideChars = r'[.,\'"%?!]'
	
	name = name.replace(" ", "-").lower()
	name = sub(invalidChars, '-', name)

	return sub(hideChars, '', name).strip("-")