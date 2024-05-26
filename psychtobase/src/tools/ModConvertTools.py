import src.Constants as Constants

def convertPack(packJson):
    return {
        "title": packJson['name'],
        "description": packJson['description'],
        "author": "Not available",
        "api_version": "0.1.0",
        "mod_version": "1.0.0",
        "license": "CC BY 4.0,MIT"
    }

def defaultPolymodMeta():
    return {
        "title": "Unknown mod",
        "description": f"Unknown mod by Unknown creator. Converted by FNF Porter v{Constants.VERSION}",
        "author": "Unknown creator",
        "api_version": "0.1.0",
        "mod_version": "1.0.0",
        "license": "CC BY 4.0,MIT"
    }

def convertCredits(text):
    lines = text.split('\n')

    result = 'Mod credits\n'

    for line in lines:
        data = line.split('::')

        if len(data) > 1:
            person = data[0]
            icon = data[1]
            roleDesc = data[2]
            social = data[3]
            color = data[4]

            result += f'{roleDesc} - {person} ({social})\n'

    return result