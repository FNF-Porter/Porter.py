from .. import Constants

def generateDescription(name:str = "Untitled Mod") -> str:
	return f"{name} by Unknown creator. Converted by FNF Porter v{Constants.VERSION}"

def convertPack(packJson):
	title = packJson.get("name", "Untitled Mod")
	description = packJson.get("description", generateDescription(title))

	return {
		"title": title,
		"description": description,
		"contributors": [],
		"dependencies": {},
		"optionalDependencies": {},
		"api_version": "0.5.0",
		"mod_version": "1.0.0",
		"license": "Apache-2.0"
	}

def defaultPolymodMeta():
	return {
		"title": "Untitled Mod",
		"description": generateDescription(),
		"contributors": [],
		"dependencies": {},
		"optionalDependencies": {},
		"api_version": "0.5.0",
		"mod_version": "1.0.0",
		"license": "Apache-2.0"
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