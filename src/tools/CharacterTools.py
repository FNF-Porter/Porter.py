import copy
import json
import logging

from .. import Constants, files
from pathlib import Path

import lxml.etree as ET 
# from src import Utils
# from src.Paths import Paths

class CharacterObject:
	def __init__(self, path, resultPath):
		self.pathName = path
		self.resultPath = resultPath

		self.characterFile = Path(path).name
		self.characterName = None
		self.iconID = None

		self.characterOrigin = [0, 0]

		self.psychCharacter:dict = {}
		self.character = copy.deepcopy(Constants.CHARACTER)

		self.loadCharacter()

	def loadCharacter(self):
		with open(self.pathName, 'r') as file:
			self.psychCharacter = json.load(file)

		self.characterJson = files.removeTrail(self.characterFile)
		self.characterName = ' '.join([string.capitalize() for string in self.characterJson.split('-')])

	def convert(self):
		characterName = self.characterName

		character = self.character
		psychCharacter = self.psychCharacter

		logging.info(f'Converting character {self.characterName}')

		character['name'] = characterName
		character['assetPath'] = psychCharacter['image']
		character['singTime'] = psychCharacter['sing_duration']

		"""
		Disable scaling. Look at https://github.com/FunkinCrew/Funkin/issues/2543 for why this exists.

		TEMPORARY FIX:
			Resize the whole spritesheet in some editing program
			Use ShadowFi's XML Resizer app: https://drive.google.com/file/d/1GoROyQKnMxiM6I0JUZ2_WKM5Aim6nY2o/view

			Eg: If the scale of your sprite was 0.6, you want to resize both Sprite Sheet and the XML to 60% of their original size.
		"""

		## It is fixed!
		self.position = psychCharacter["position"]
		scale = psychCharacter['scale']

		character['scale'] = scale

		character['isPixel'] = psychCharacter['scale'] >= 6
		character['healthIcon']['id'] = psychCharacter['healthicon']
		character['healthIcon']['isPixel'] = psychCharacter['scale'] >= 6
		character['flipX'] = psychCharacter.get('flip_x', False)

		self.iconID = psychCharacter['healthicon']

		# I love object oriented programming and making a million variables for no reason!
		idleAnim = None
		idlePrefix = None

		for animation in psychCharacter['animations']:
			curAnim = animation.get("anim", None)
			if curAnim == "idle" or curAnim == "danceLeft":
				idleAnim = animation
				idlePrefix = animation.get("name", None)

			animTemplate = copy.deepcopy(Constants.ANIMATION)

			animTemplate['name'] = animation['anim']
			animTemplate['prefix'] = animation['name']
			animTemplate['offsets'] = animation['offsets']
			animTemplate['frameRate'] = animation['fps']
			animTemplate['frameIndices'] = animation['indices']

			# Note to remove this later
			logging.info(f'[{characterName}] Converting animation {animation}')

			self.character['animations'].append(animTemplate)

		# STILL WORKING ON IT
		if idlePrefix != None:
			quickPath = Path(self.pathName)
			xmlPath = quickPath.parent.parent / f"images/{psychCharacter['image']}.xml"

			if xmlPath.exists():
				xml = ET.parse(xmlPath).getroot()
				lastFrameIDX = -1

				if idleAnim != None:
					print(idleAnim.get("indices"))
					indices = idleAnim.get("indices")
					if (indices != None and len(indices) > 0):
						lastFrameIDX = indices[-1]

				frames = [child for child in xml if idlePrefix in child.attrib.get("name", "")]
				lastFrame = frames[lastFrameIDX].attrib

				self.characterOrigin = [
					float(lastFrame.get("width")) * scale / 2,
					float(lastFrame.get("height")) * scale
				]

				print(self.characterOrigin)

		logging.info(f'Character {characterName} successfully converted')

	def save(self):
		savePath = Path(self.resultPath) / self.characterJson

		logging.info(f'Character {self.characterName} saved to {savePath}.json')

		with open(f'{savePath}.json', 'w') as f:
			json.dump(self.character, f, indent=4)

characters:dict[str, CharacterObject] = {}

def createCharacter(path:Path, savePath:str):
	name = path.stem

	newCharData = CharacterObject(path, savePath)
	characters[name] = newCharData

	return newCharData