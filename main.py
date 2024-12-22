import json
import logging
import shutil
import threading
import time

from base64 import b64decode
from pathlib import Path
from PIL import Image

from src import UI, Constants, FileContents, files, log, Utils

from src.tools import StageLuaParse, StageTool, VocalSplit, WeekTools
from src.tools import ModConvertTools as ModTools

from src.tools import CharacterTools
from src.tools import ChartTools 

from src.lua.Objects import LuaScript
from src.tools import StageTools

root = Path(__file__).parent

def fileCopy(source, destination):
	"""
	Copies a file to a destination
	
	Args:
		source (str): Path to the file.
		destination (str): Path to where the file should go.
	"""
	if Path(source).exists():
		try:
			shutil.copyfile(source, destination)
		except Exception as e:
			logging.error(f'Something went wrong: {e}')
	else:
		logging.warn(f'Path {source} doesn\'t exist.')

def convert():
	window = UI.window

	runtime = time.time()

	inputMod = Path(window.modLineEdit.text())
	outputFolder = Path(window.baseGameLineEdit.text())

	modName = inputMod.name
	outputMod = outputFolder.joinpath(modName)
	print(outputMod)
	outputMod.mkdir(exist_ok = True)

	options = window.generateOptionsMap()

	# Announces a large string of text indicating the conversion has began.
	logging.info(Utils.coolText("NEW CONVERSION STARTED"))
	logging.debug(f"Option data: {options}")

	logging.info(f'Converting from {inputMod} to {outputFolder}')

	# Accesses the options to see if the user selected modpack metadata
	if options.get('modpack_meta'):

		# `pack.json` convesion code

		logging.info('Converting pack.json')

		# Define `pack.json` paths
		psychPack, polymodMetaDir = Constants.FILE_LOCS.get('PACKJSON')
		psychPackPath = inputMod.joinpath(psychPack)
		polymodMetaPath = outputMod.joinpath(polymodMetaDir)

		# try-except fail mechanism
		try:
			if psychPackPath.exists():
				polymod_meta = ModTools.convertPack(json.loads(psychPackPath.read_text()))
			else:
				logging.warning("pack.json wasn't found. Replacing pack with DEFAULT")
				polymod_meta = ModTools.defaultPolymodMeta()

			polymodMetaPath.write_text(json.dumps(polymod_meta, indent = 4))
			logging.info('pack.json successfully converted and saved!')

		except Exception as e:
			logging.error("Couldn't convert pack.json file")

		# `pack.png` conversion code

		logging.info('Copying pack.png')

		# Define `pack.png` paths
		psychIcon, polymodIcon = Constants.FILE_LOCS.get('PACKPNG')
		psychIconFile = inputMod.joinpath(psychIcon)
		polymodIconFile = outputMod.joinpath(polymodIcon)

		# try-except fail mechanism
		try:
			if psychIconFile.exists():
				fileCopy(psychIconFile, polymodIconFile)
			else:
				# If the file does not exist, replace it with a default one
				logging.warning("pack.png wasn't found! Using DEFAULT instead.")

				with polymodIconFile.open("wb") as f:
					f.write(b64decode(Constants.BASE64_IMAGES.get('missingModImage')))

		except Exception as e:
			logging.error(f'Unable to copy pack.png file: {e}')

		# `credits.txt` conversion code

		logging.info('Parsing and converting credits.txt')

		# Define `credits.txt` paths
		psychCredits, modCredits = Constants.FILE_LOCS.get('CREDITSTXT')
		psychCreditsPath = inputMod.joinpath(psychCredits)
		baseCreditsPath = outputMod.joinpath(modCredits)

		# Find credits' mere existence.
		if psychCreditsPath.exists():
			resultCredits = ModTools.convertCredits(psychCreditsPath.read_text())
			baseCreditsPath.write_text(resultCredits)
		else:
			logging.warning(f'Unable to find {psychCreditsPath}!')

	# Complete the conversion by announcing it has completed
	logging.info(Utils.coolText("CONVERSION COMPLETED"))

	# Announce how long it took to convert it
	logging.info(f'Conversion was finished! Mod was converted in {time.time() - runtime}s')

if __name__ == '__main__':
	app = UI.init()

	UI.window.addOnButtonEvent(convert)
	app.exec()