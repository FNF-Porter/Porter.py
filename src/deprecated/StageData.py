from ..Constants import STAGE, STAGE_PROP, STAGE_PROP_ANIMATED, STAGE_PROP_ANIMATION, STAGE_PROP_IMAGE

from copy import deepcopy

stages = {}

def createStage(name:str):

	newStageData = deepcopy(STAGE)
	newStageData["name"] = name

	stages[name] = newStageData

createStage("cock")
print(stages)