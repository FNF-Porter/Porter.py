import json
import logging
import copy
from pathlib import Path
from psychtobase.src import window, Constants
from psychtobase.src import files

class CharacterObject:
	def __init__(self, path: str, resultPath) -> None:
		self.charName:str = Path(path).name
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

		logging.info(f'Converting character {self.charName}')

		englishCharacterName = ' '.join([string.capitalize() for string in self.characterJson.split('-')])
		self.character['name'] = englishCharacterName
		self.character['assetPath'] = char['image']
		self.character['singTime'] = char['sing_duration']
		self.character['scale'] = char['scale']
		self.character['isPixel'] = char['scale'] >= 6
		self.character['healthIcon']['id'] = char['healthicon']
		self.character['healthIcon']['isPixel'] = char['scale'] >= 6
		self.character['flipX'] = char.get('flip_x', False)

		#i love object oriented programming and making a million variables for no reason!
		for animation in char['animations']:
			animTemplate = copy.deepcopy(Constants.ANIMATION)

			animTemplate['name'] = animation['anim']
			animTemplate['prefix'] = animation['name']
			animTemplate['offsets'] = animation['offsets']

			logging.info(f'[{englishCharacterName}] Converting animation {animation}')
			#note to remove this later

			self.character['animations'].append(animTemplate)

		logging.info(f'Character {englishCharacterName} successfully converted')

	def save(self):
		savePath = Path(self.resultPath) / self.characterJson

		logging.info(f'Character {self.characterName} saved to {savePath}.json')

		with open(f'{savePath}.json', 'w') as f:
			json.dump(self.character, f, indent=4)