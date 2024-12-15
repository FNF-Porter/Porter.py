import json
from pathlib import Path

class Paths:
	assetsDir = ''

	@staticmethod 
	def getPath(file:str, library:str = None):
		if library != None:
			return Paths.getLibraryPath(file, library)

		return Paths.getPreloadPath(file)

	@staticmethod
	def getLibraryPath(file:str, library:str = 'preload'):
		if (library == 'preload'):
			return Paths.getPreloadPath(file)
		return Paths.getLibraryPathForce(file, library)

	getLibraryPathForce = staticmethod(lambda file, library: Path(Paths.assetsDir, library, file))
	getPreloadPath = staticmethod(lambda file: Paths.assetsDir / Path(file))

	txt = staticmethod(lambda key, library=None: Paths.getPath(f'{key}.txt', library))
	xml = staticmethod(lambda key, library=None: Paths.getPath(f'{key}.xml', library))
	json = staticmethod(lambda key, library=None: Paths.getPath(f'{key}.json', library))

	@staticmethod
	def parseJson(file: str):
		try:
			with open(Paths.json(file), 'r') as f:
				return json.load(f)
		except Exception as e:
			print(f"Error! {e}")

	@staticmethod
	def writeJson(file:str, writeFile:dict, indent:int = 4):
		try:
			with open(Paths.json(file), 'w') as f:
				return json.dump(writeFile, f, indent = indent)
		except Exception as e:
			print(f"Error! {e}")

	@staticmethod
	def openFile(file: str):
		try:
			with open(Paths.getPath(file), 'r') as f:
				return f.read()
		except Exception as e:
			print(f"ERROR | {e}")
			return None

	@staticmethod
	def join(*path) -> str:
		return str(Path(path[0]).joinpath(*path[1:]))