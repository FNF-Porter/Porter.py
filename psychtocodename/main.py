import os
import sys
from src.XMLTools import CharacterXML
from src.Paths import Paths

rootDir = os.path.join(os.path.dirname(__file__))

modName = sys.argv[1]
modDir = os.path.join(rootDir, "mods", modName)
saveDir = os.path.join(rootDir, "output", modName)

os.chdir(rootDir)
Paths.assetsDir = os.path.join(".\mods", modName)

try: os.mkdir(f"{saveDir}/data/characters")
except FileExistsError: pass

print("Beginning conversion to xml...")
for file in os.listdir(os.path.join(modDir, "characters")):
	if not file.endswith(".json"):
		continue

	char = file[:-5]
	path = os.path.join(modDir, "characters", char)

	xml = CharacterXML().setup(path)
	xml.save(os.path.join(saveDir, "data", "characters"))

	print(f"> {char.replace('-', ' ').upper()} Converted!")

print("Conversion complete!")