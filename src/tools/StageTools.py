"""
	Creates new stage data for Base Funkin'
"""

from copy import deepcopy

from ..Constants import STAGE, STAGE_PROP, STAGE_CHARACTER_DATA, STAGE_PROP_ANIMATION, STAGE_PROP_IMAGE
from ..lua.Objects import SpriteData
from ..Utils import compareDicts

from . import CharacterTools

def buildStage(name:str, json, spriteData:SpriteData):
	"""
		Function to create stage data based on sprite information from a LUA script
	"""

	stageMetadata = deepcopy(STAGE)

	props = stageMetadata["props"]
	characters = stageMetadata["characters"]

	stageMetadata["name"] = name
	stageMetadata["cameraZoom"] = json.get("defaultZoom", 1)

	for prop, data in spriteData.get().items():
		# data["position"][1] -= 720

		propData = deepcopy(STAGE_PROP)

		propData["name"] = prop
		propData["assetPath"] = data["path"]
		propData["position"] = data["position"]
		propData["zIndex"] = data["zIndex"]
		propData["scale"] = data["scale"]
		propData["scroll"] = data.get("scroll", [1, 1])

		for animation in data.get("animations", []):
			anim = deepcopy(STAGE_PROP_ANIMATION)
			anim.update(animation)

			compareDicts(anim, STAGE_PROP_ANIMATION)
			propData["animations"].append(anim)

		compareDicts(propData, STAGE_PROP, ["position"])
		props.append(propData)

	characters["bf"]["position"] = json["boyfriend"]
	characters["dad"]["position"] = json["opponent"]
	characters["gf"]["position"] = json["girlfriend"]

	for char in characters.values():
		compareDicts(char, STAGE_CHARACTER_DATA, ["cameraOffsets"])

	compareDicts(stageMetadata, STAGE, ["version"])

	return stageMetadata

stages = {}

def createStage(name:str, json, spriteData:SpriteData):

	newStageData = buildStage(name, json, spriteData)
	stages[name] = newStageData

	return newStageData