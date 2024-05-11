import copy
import src.Constants as Constants
import src.window as window

def convert(stageJSON, assetName):
    stageTemplate = copy.deepcopy(Constants.STAGE)

    stageTemplate['cameraZoom'] = stageJSON['defaultZoom']
    stageTemplate['characters']['bf']['position'] = stageJSON['boyfriend']
    stageTemplate['characters']['gf']['position'] = stageJSON['girlfriend']
    stageTemplate['characters']['dad']['position'] = stageJSON['opponent']

    stageTemplate['name'] = window.prompt('input', f'Enter the name of {assetName}', [['Stage Name', 'Your Stage Name']], 'StageTool.py')[0]

    return stageTemplate