import json
from lxml import etree
import os
import utils

class XMLFile(etree.ElementBase):

	defaultAttr = {}
	# renameValues = {} screw this

	@property
	def doctype(self):
		return f"<!DOCTYPE codename-engine-{self._xmlType}>"

	def _init(self):
		self.tag = "root"
		self._xmlType = "root"
		self.fileName = None

		self.json = None

	def setup(self, directory:str):
		self.fileName = directory
		for cuh, aaa in self.defaultAttr.items():
			self.attrib[cuh] = aaa
		return self

	def basicCheck(self, key:str, val:any):
		# key = self.renameValues.get(key, key)
		val = utils.toString(val)

		if self.attrib[key] == val:
			del self.attrib[key]
		else:
			self.attrib[key] = val
		
	def advancedCheck(self, values:dict):
		for key, val in values.items():
			self.basicCheck(key, val)

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
		"icon": "",
		"scale": "1",
		"antialiasing": "true",
		"sprite": ""
	}

	def _init(self):
		self.tag = "character"
		self._xmlType = "character"

	def setup(self, directory:str):
		super().setup(directory)
		self.character = os.path.basename(directory)
		self.attrib["icon"] = self.character
		self.attrib["sprite"] = self.character

		self.loadFromJson()

		return self

	def loadFromJson(self):
		super().loadFromJson()

		json = self.json
		animations = json.pop("animations")
		position = json.pop("position")
		camera_position = json.pop("camera_position")

		self.advancedCheck({
			"isPlayer": self.character.startswith("bf"),
			"isGF": self.character.startswith("gf"),
			"x": position[0],
			"y": position[1],
			"camx": camera_position[0],
			"camy": camera_position[1],
			"holdTime": json.get("sing_duration"),
			"flipX": json.get("flip_x"),
			"icon": json.get("healthicon"),
			"scale": json.get("scale"),
			"antialiasing": not json.get("no_antialiasing"),
			"sprite": os.path.basename(json.get("image"))
		})

		for anim in animations:
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