from lupa import LuaRuntime
from lupa import LuaError
from pathlib import Path

import logging

class SpriteData:
	def __init__(self):
		self.data:dict[str, any] = {}
		self.objectOrder:list = []

		self.idxCounter = 0

		self.callbacks = {
			"makeLuaSprite": self.makeLuaSprite,
			"addLuaSprite": self.addLuaSprite,
			"makeAnimatedLuaSprite": self.makeAnimatedLuaSprite,
			"addAnimationByPrefix": self.addAnimationByPrefix,
			"scaleObject": self.scaleObject,
			"setScrollFactor": self.setScrollFactor
		}

	def get(self) -> dict[str, any]:
		return self.data

	def getCallbacks(self) -> dict:
		return self.callbacks

	def makeLuaSprite(self, tag, path, x, y):
		self.data[tag] = {
			"path": path,
			"position": [x, y],
			"zIndex": 0,
			"scale": [1, 1]
		}
	
	def addLuaSprite(self, tag, inFront = False):
		if self.data.get(tag) == None:
			return

		self.data[tag]["inFront"] = inFront
		self.objectOrder.append(self.data[tag])

	def makeAnimatedLuaSprite(self, tag, path = None, x = 0, y = 0):
		self.data[tag] = {
			"path": path,
			"position": [x, y],
			"zIndex": 0,
			"scale": [1, 1],
			"scroll": [1, 1],
			"animations": []
		}

	def addAnimationByPrefix(self, tag, name, prefix, fps, looped = True):
		if self.data[tag].get("animations") == None:
			return

		self.data[tag]["animations"].append(
			{
				"name": name,
				"prefix": prefix,
				"fps": fps,
				"looped": looped
			}
		)

	def scaleObject(self, tag, sx, sy):
		self.data[tag]["scale"] = [sx, sy]

	def setScrollFactor(self, tag, sx, sy):
		self.data[tag]["scroll"] = [sx, sy]

class LuaScript(LuaRuntime):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.stageName = ""
		self.spriteData = SpriteData()

		for name, callback in self.spriteData.getCallbacks().items():
			self.globals()[name] = callback

		self.globals()["FPORTER_missing"] = self.FPORTER_missing

		self.__setup_metatable__()

	def FPORTER_missing(self, name, *args):
		logging.warning(f"Missing callback from {self.stageName}! {name}{args}")

	def __setup_metatable__(self):
		self.execute("""
		setmetatable(_G, {
			__index = function(_, key)
				return function(...)
					return FPORTER_missing(key, ...)
				end
			end
		})
		""")

	def init(self, file:Path):
		try:
			self.stageName = file.stem
			self.execute(file.read_text())

		except LuaError as e:
			logging.warning(f"Parsing Error! {e}")

		except Exception as e:
			logging.warning(f"Error! {e}")

		if 'onCreate' in self.globals():
			self.globals().onCreate()

		objs = self.spriteData.objectOrder

		for i, obj in enumerate(objs):
			if obj["inFront"]:
				obj["zIndex"] = 300 + i
			else:
				obj["zIndex"] = i - len(objs)

		return self