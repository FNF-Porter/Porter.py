import json
from lxml import etree
import os
from src import Utils
from src.Paths import Paths

class XMLFile(etree.ElementBase):

	defaultAttr:dict[str] = {}
	# renameValues = {} screw this

	@property
	def doctype(self) -> str:
		return f"<!DOCTYPE codename-engine-{self._xmlType}>"

	def _init(self):
		self.tag:str = "root"
		self._xmlType:str = "root"
		self.fileName:str = None

		self.json:dict = None

	def setup(self, directory:str):
		self.fileName = directory
		for cuh, aaa in self.defaultAttr.items():
			self.attrib[cuh] = aaa
		return self

	def basicCheck(self, key:str, val:any):
		# key = self.renameValues.get(key, key)
		val = Utils.toString(val)

		attrib = self.attrib.get(key)
		if attrib != None and attrib == val:
			del self.attrib[key]
		else:
			self.attrib[key] = val
		
	def advancedCheck(self, values:dict):
		for key, val in values.items():
			self.basicCheck(key, val)

	def loadFromJson(self):
		if (self.fileName == None):
			return

		self.json = Paths.parseJson(self.fileName)

	def save(self, directory:str):
		etree.ElementTree(self).write(f"{directory}.xml", pretty_print=True, doctype=self.doctype)
	
class CharacterXML(XMLFile):
	"""
	Default Codename Engine character XML
	"""

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
		self.character:str = os.path.basename(directory)
		self.attrib["icon"] = self.character
		self.attrib["sprite"] = self.character

		self.loadFromJson()

		return self

	def loadFromJson(self):
		super().loadFromJson()

		json:dict = self.json
		animations:list[dict] = json.pop("animations")
		position:list[int] = json.pop("position")
		camera_position:list[int] = json.pop("camera_position")

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
		directory = os.path.join(directory, self.character)
		super().save(directory)

class WeekXML(XMLFile):
	"""
	Default Codename Engine Week XML
	"""

	defaultAttr = {"difficulties": "easy,normal,hard"}

	def _init(self):
		self.tag = "week"
		self._xmlType = "week"

	def setup(self, directory:str):
		super().setup(directory)
		self.loadFromJson()

		return self

	def loadFromJson(self):
		super().loadFromJson()
		json:dict = self.json

		if (json.get("hideStoryMode")):
			return

		songs:list[dict] = json.pop("songs")
		weekCharacters:list[int] = json.pop("weekCharacters")

		print("what")

		self.advancedCheck({
			"name": json.get("storyName"),
			"sprite": os.path.basename(self.fileName),
			"chars": ",".join(weekCharacters),
			"difficulties": json.get("difficulties")
		})

		for song in songs:
			etree.SubElement(self, "song").value = song[0]