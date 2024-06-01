import copy
import json
import logging

from .. import Constants, files
from pathlib import Path

# import lxml.etree as ET 
# from src import Utils
# from src.Paths import Paths

class CharacterObject:
	def __init__(self, path, resultPath):
		self.pathName = path
		self.resultPath = resultPath

		self.characterFile = Path(path).name
		self.characterName = None
		self.iconID = None

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

		character['scale'] = psychCharacter['scale']
		"""

		character['isPixel'] = psychCharacter['scale'] >= 6
		character['healthIcon']['id'] = psychCharacter['healthicon']
		character['healthIcon']['isPixel'] = psychCharacter['scale'] >= 6
		character['flipX'] = psychCharacter.get('flip_x', False)

		self.iconID = psychCharacter['healthicon']

		# I love object oriented programming and making a million variables for no reason!
		for animation in psychCharacter['animations']:
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
		# file = Paths.openFile(Paths.join(Utils.getModPath(), "images", self.psychCharacter.get("image", "")) + ".xml")
		# if file != None:
		# 	xml = ET.iterparse(file)

		logging.info(f'Character {characterName} successfully converted')

	def save(self):
		savePath = Path(self.resultPath) / self.characterJson

		logging.info(f'Character {self.characterName} saved to {savePath}.json')

		with open(f'{savePath}.json', 'w') as f:
			json.dump(self.character, f, indent=4)