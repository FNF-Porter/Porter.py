import json
from lxml import etree
import os

class XMLFile(etree.ElementBase):

	defaultAttr = {}
	# renameValues = {} Will be reused later

	@property
	def doctype(self):
		return f"<!DOCTYPE codename-engine-{self._xmlType}>"

	def _init(self):
		self.tag = "root"
		self._xmlType = "root"
		self.fileName = None

		self.json = None

	def setup(self):
		return self
	
	@staticmethod
	def toString(val:any) -> str:
		"""
		Converts any value to a string
		"""

		instance = type(val)
		if instance == str:
			return val
		val = str(val)
		if instance == bool:
			return val.lower()
		return val

	def defaultCheck(self, key:str, val:any, dictionary:dict=None):
		if (dictionary is None):
			dictionary = self.defaultAttr

		val = self.toString(val)

		if dictionary.get(key) == val:
			if self.attrib.get(key) is not None:
				del self.attrib[key]
		else:
			self.attrib[key] = val

	def loadFromJson(self):
		if (self.fileName == None):
			return

		with open(f"{self.fileName}.json", "r") as f:
			self.json = json.load(f)
			f.close()

	def save(self, file):
		etree.ElementTree(self).write(file, pretty_print=True, doctype=self.doctype)
	
class CharacterXML(XMLFile):

	# Default Codename Engine character XML

	defaultAttr = {
		"isPlayer": "false",
		"isGF": "false",
		"x": "0",
		"y": "0",
		"camx": "0",
		"camy": "0",
		"holdTime": "4",
		"flipX": "false",
		"icon": None,
		"scale": "1",
		"antialiasing": "true",
		"sprite": None
	}

	def _init(self):
		self.tag = "character"
		self._xmlType = "character"

	def setup(self, directory:str):
		self.fileName = directory
		self.character = os.path.basename(directory)
		self.loadFromJson()

		return self

	def loadFromJson(self):
		super().loadFromJson()

		json = self.json

		position = json.get("position")
		camera_position = json.get("camera_position")

		self.defaultCheck("isPlayer", self.character.startswith("bf"))
		self.defaultCheck("isGF", self.character.startswith("gf"))

		self.defaultCheck("x", position[0])
		self.defaultCheck("y", position[1])

		self.defaultCheck("camx", camera_position[0])
		self.defaultCheck("camy", camera_position[1])

		self.defaultCheck("holdTime", json.get("sing_duration"))
		self.defaultCheck("flipX", json.get("flip_x"))
		self.defaultCheck("icon", json.get("healthicon"), {"icon": self.character})
		self.defaultCheck("scale", json.get("scale"))
		self.defaultCheck("antialiasing", not json.get("no_antialiasing"))
		self.defaultCheck("sprite", os.path.basename(json.get("image")), {"sprite": self.character})

		for anim in json.get("animations"):
			offsets = anim.get("offsets")
			indices = ",".join(str(frame) for frame in anim.get("indices"))

			subAnim = etree.SubElement(self, "anim", {
				"name": anim.get("name"),
				"anim": anim.get("anim"),
				"fps": str(anim.get("fps")),
				"loop": str(anim.get("loop")).lower(),
				"x": str(offsets[0]),
				"y": str(offsets[1])
			})

			if len(indices) > 0:
				subAnim.attrib["indices"] = indices

	def save(self, directory:str):
		etree.ElementTree(self).write(f"{os.path.join(directory, self.character)}.xml", pretty_print=True, doctype=self.doctype)