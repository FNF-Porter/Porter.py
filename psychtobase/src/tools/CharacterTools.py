import json
import os
import logging
from psychtobase.src import window, Constants
from psychtobase.src import files

class CharacterObject:
	def __init__(self, path: str, resultPath) -> None:
		self.charName:str = os.path.basename(path)
		self.resultPath = resultPath
		self.pathName:str = path
		self.psychChar = {}
		self.character:dict = Constants.CHARACTER.copy()
		self.characterName:str = None

		self.loadCharacter()

	def loadCharacter(self):
		self.psychChar = json.loads(open(self.pathName, 'r').read())
		self.characterJson = files.removeTrail(self.charName)

	def convert(self):
		char = self.psychChar

		logging.info(f'Requesting information for {self.charName}')

		character_name = window.prompt('input', f'Enter {self.characterJson}\'s name', [['Character Name', 'Your Character Name']], 'character.py')
		self.characterName = character_name[0]

		logging.info(f'Converting character {self.charName}')

		self.character['assetPath'] = char['image']
		self.character['singTime'] = char['sing_duration']
		self.character['scale'] = char['scale']
		self.character['isPixel'] = char['scale'] >= 6
		self.character['healthIcon']['id'] = char['healthicon']
		self.character['healthIcon']['isPixel'] = char['scale'] >= 6

		for animation in char['animations']:
			animTemplate = Constants.ANIMATION.copy()

			animTemplate['name'] = animation['anim']
			animTemplate['offsets'] = animation['offsets']
			animTemplate['prefix'] = animation['name']

			self.character['animations'].append(animTemplate)

		logging.info(f'Character {character_name[0]} successfully converted')

	def save(self):
		savePath = os.path.join(self.resultPath, self.characterJson)

		logging.info(f'Character {self.characterName} saved to {savePath}.json')

		with open(f'{savePath}.json', 'w') as f:
			json.dump(self.character, f, indent=4)