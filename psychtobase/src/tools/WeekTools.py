import copy
import json
import logging
import src.Constants as Constants

def convert(weekJSON, modfolder):
    level = copy.deepcopy(Constants.LEVEL)

    level['name'] = weekJSON['storyName']
    levelSongs = []
    for song in weekJSON['songs']:
        levelSongs.append(song[0])

    level['songs'] = levelSongs

    for char in weekJSON['weekCharacters']:
        if defaultProp(char):
            level['props'].append(defaultProp(char))
        else:
            weekCharJSONStr = ''
            logging.info(f'Opening {char}.json')
            try:
                weekCharJSONStr = open(modfolder + Constants.FILE_LOCS.get('WEEKCHARACTERJSON')[0] + f'{char}.json').read()
            except:
                logging.error(f'Could not open {char}.json')
                continue
            weekCharacterJSON = json.loads(weekCharJSONStr)

            propTemplate = copy.deepcopy(Constants.LEVEL_PROP)
            propTemplate['assetPath'] = Constants.FILE_LOCS.get('WEEKCHARACTERASSET')[1] + weekCharacterJSON['image']
            propTemplate['scale'] = weekCharacterJSON['scale']
            propTemplate['offsets'] = weekCharacterJSON['position']
            propTemplate['animations'] = []

            idleTemplate = copy.deepcopy(Constants.LEVEL_PROP_ANIMATION)
            idleTemplate['name'] = 'idle'
            idleTemplate['prefix'] = weekCharacterJSON['idle_anim']
            propTemplate['animations'].append(idleTemplate)

            if len(weekCharacterJSON.get('confirm_anim', 0)) > 0 or weekCharacterJSON['confirm_anim']:
                confirmTemplate = copy.deepcopy(Constants.LEVEL_PROP_ANIMATION)
                confirmTemplate['name'] = 'confirm'
                confirmTemplate['prefix'] = weekCharacterJSON['confirm_anim']
                propTemplate['animations'].append(confirmTemplate)

            level['props'].append(propTemplate)
    
    level['background'] = '#FFFFFF' # Change!!

    return level

def defaultProp(propName):
    return Constants.LEVEL_PROP_DEFAULTS.get(propName, None)