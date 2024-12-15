"""
A class full of tools needed for mod conversion.
"""

import time
import webbrowser

from . import Constants
from re import sub

def getRuntime(start:float) -> float:
	"""
	Small function to keep track of runtime
	"""
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

def event(time:float, event:str, values:dict) -> dict:
	"""
	Function created for faster creation of events.
	"""
	return {"t": time, "e": event, "v": values}

def changeCharacter(time:float, target: str, char: str):
	"""
	Function created for faster creation of Change Character events
	"""
	return event(time, "Change Character", {"target": target, "char": char})

def focusCamera(time:float, char:bool):
	"""
	Function created for faster creation of camera change events.
	"""
	return event(time, "FocusCamera", {"char": "0" if char else "1"})

def playAnimation(time:float, target: str, anim: str, force: bool):
	"""
	Function created for faster creation of Play Animation events
	"""
	return event(time, "PlayAnimation", {"target": target, "anim": anim, "force": force}) # Force is enabled on Play Animation events, not Alt Animation

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

	return sub(hideChars, '', name)

def compareDicts(dict1:dict, dict2:dict, exclude:list = []):
	"""
		Compares 2 dictionaries, and removes optional data.
		Use exclude to keep things you don't want overwritten!
	"""
	for k, v in dict2.items():
		if dict1.get(k, None) == v and exclude.count(k) < 1:
			del dict1[k]

def createUrl(*urlElements: str) -> str:
	"""
	Returns a URL from the given elements.
	Use `openUrl()` to open it in a browser.
	"""
	return "/".join(urlElements)

def openUrl(*urlElements: str) -> str:
	"""
	Opens a page URL in your preferred browser.
	Returns your URL as a string.
	"""
	url = createUrl(*urlElements)
	webbrowser.open(url)
	return url

# def setModPath(name:str):
# 	global modPath
# 	modPath = name

# def getModPath() -> str:
# 	return modPath