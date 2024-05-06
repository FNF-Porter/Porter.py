import json
import log
import copy
import files as filename
import window

characterTemplate = {
    "version": "1.0.0",
    "name": None,
    "assetPath": None,
    "singTime": None,
    "isPixel": None,
    "scale": None,
    "healthIcon": {
        "id": None,
        "isPixel": None,
        "flipX": False,
		"scale": 1
    },
    "animations": []
}

animationTemplate = {
    "name": None,
    "prefix": None,
    "offsets": [0, 0]
}

def character_convert(file):
    char = json.loads(open(file, 'r').read())
    char_name = filename.removeTrail(file)

    template = copy.deepcopy(characterTemplate)

    log.log_line('convert/character.py', f'Requesting information for {char_name}')

    character_name = window.prompt('input', f'Enter {char_name}\'s name', [['Character Name', 'Your Character Name']], 'character.py')

    log.log_line('convert/character.py', f'Converting character {char_name}')

    template['name'] = character_name[0]
    template['assetPath'] = char['image']
    template['singTime'] = char['sing_duration']
    template['scale'] = char['scale']
    template['isPixel'] = char['scale'] >= 6
    template['healthIcon']['id'] = char['healthicon']
    template['healthIcon']['isPixel'] = char['scale'] >= 6

    for animation in char['animations']:
        animTemplate = copy.deepcopy(animationTemplate)

        animTemplate['name'] = animation['anim']
        animTemplate['offsets'] = animation['offsets']
        animTemplate['prefix'] = animation['name']

        template['animations'].append(animTemplate)

    log.log_line('convert/character.py', f'Character {char_name} successfully converted')

    return template