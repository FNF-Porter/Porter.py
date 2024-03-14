import json
from lxml import etree
import os
import utils

class XMLFile(etree.ElementBase):

	defaultAttr = {}
	renameValues = {}

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

	def defaultCheck(self, key:str, val:any, dictionary:dict=None):
		if (dictionary is None):
			dictionary = self.defaultAttr

		key = self.renameValues.get(key, key)
		val = utils.toString(val)

		dKey = dictionary.get(key)
		if dKey == val and self.attrib.get(key) is not None:
			del self.attrib[key]
		elif dKey != val:
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

	renameValues = {
		"sing_duration": "holdTime",
		"flip_x": "flipX",
		"healthicon": "icon",
		"no_antialiasing": "antialiasing",
		"image": "sprite"
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

		self.defaultCheck("isPlayer", self.character.startswith("bf"))
		self.defaultCheck("isGF", self.character.startswith("gf"))

		for key, item in json.items():
			match(key):
				case "animations":
					for anim in item:
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
				case "position":
					self.defaultCheck("x", item[0])
					self.defaultCheck("y", item[1])
				case "camera_position":
					self.defaultCheck("camx", item[0])
					self.defaultCheck("camy", item[1])
				case "healthbar_colors":
					continue
				case "healthicon":
					self.defaultCheck(key, item, {"icon": self.character})
				case "image":
					self.defaultCheck(key, os.path.basename(item), {"sprite": self.character})
				case "no_antialiasing":
					self.defaultCheck(key, not item)
				case _:
					self.defaultCheck(key, item)

	def save(self, directory:str):
		etree.ElementTree(self).write(f"{os.path.join(directory, self.character)}.xml", pretty_print=True, doctype=self.doctype)