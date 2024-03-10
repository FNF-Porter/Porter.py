import json
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as Dom

cneStruct:dict = { # Default Codename Engine character XML
	"isPlayer": "false",
	"isGF": "false",
	"x": "0",
	"y": "0",
	"camx": "0",
	"camy": "0",
	"holdTime": "4",
	"flipX": "false",
	"icon": None,
	"scale": "1",
	"antialiasing": "true",
	"sprite": None
}

def defCheck(dict:dict, key:str, val:str) -> dict:
	if dict.get(key) == val:
		del dict[key]
	else:
		dict[key] = val

rootDir = os.path.join(os.path.dirname(__file__))
os.chdir(rootDir)

try: os.mkdir("results")
except FileExistsError: pass

while True:
	modName = input("Enter your mod folder name: ")
	modDir = os.path.join(rootDir, modName)
	if os.path.exists(modName):
		break
	print("Mod not found.. try again.")

print("Beginning conversion...")
for file in os.listdir(os.path.join(modName, "characters")):
	if not file.endswith(".json"):
		continue

	char = file[:-5]
	charStruct = cneStruct.copy()

	with open(os.path.join(modDir, "characters", file), "r") as f:
		jsonFile = json.load(f)
		f.close()

	charStruct["icon"] = char
	charStruct["sprite"] = char

	position = jsonFile.get("position")
	camera_position = jsonFile.get("camera_position")
	
	defCheck(charStruct, "isPlayer",     str(char.startswith("bf")).lower())
	defCheck(charStruct, "isGF",         str(char.startswith("gf")).lower())
	defCheck(charStruct, "x",            str(position[0]))
	defCheck(charStruct, "y",            str(position[1]))
	defCheck(charStruct, "camx",         str(camera_position[0]))
	defCheck(charStruct, "camy",         str(camera_position[1]))
	defCheck(charStruct, "holdTime",     str(jsonFile.get("sing_duration")))
	defCheck(charStruct, "flipX",        str(jsonFile.get("flip_x")).lower())
	defCheck(charStruct, "icon",         jsonFile.get("healthicon"))
	defCheck(charStruct, "scale",        str(jsonFile.get("scale")))
	defCheck(charStruct, "antialiasing", str(not jsonFile.get("antialiasing")).lower())
	defCheck(charStruct, "sprite",       os.path.basename(jsonFile.get("image")))

	xml = ET.Element("character", charStruct)
	for anim in jsonFile.get("animations"):
		offsets = anim.get("offsets")
		indices = ",".join(str(frame) for frame in anim.get("indices"))

		ET.SubElement(xml, "anim", {
			"name": anim.get("name"),
			"anim": anim.get("anim"),
			"fps": str(anim.get("fps")),
			"loop": str(anim.get("loop")).lower(),
			"x": str(offsets[0]),
			"y": str(offsets[1])
		})

		if len(indices) > 0:
			xml.attrib["indices"] = indices

	# Forgive me for this garbage code brah 😭😭😭
	xmlString = f"<!DOCTYPE codename-engine-character>\n{ET.tostring(xml).decode('utf-8')}"
	xmlString = "\n".join(line for line in Dom.parseString(xmlString).toprettyxml().split("\n")[1:] if line.strip())
	with open(f"results/{char}.xml", "w") as f:
		f.write(xmlString)
		f.close()

	print(f"> {char.replace('-', ' ').upper()} Converted!")

print("Conversion complete!")