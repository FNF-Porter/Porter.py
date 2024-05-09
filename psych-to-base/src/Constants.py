"""
A class full of constants needed for chart conversion.
"""

DIFFICULTIES:list = ["easy", "normal", "hard"]

STAGES = {
	"stage": "mainStage"
}

CHARACTERS = {
	"pico-player": "pico-playable"
}

BASE_CHART_METADATA = {
	"version": "2.2.0",
	"songName": "",
	"artist": "Unknown",
	"looped": False,

	"offsets": {
		"instrumental": 0,
		"altInstrumentals": {},
		"vocals": {}
	},

	"playData": {
		"album": "volume1",
		"previewStart": 0,
		"previewEnd": 15000,
		"songVariations": [],
		"difficulties": [],
		"characters": {
			"album": "volume1",
			"player": "bf",
			"girlfriend": "gf",
			"opponent": "dad",
			"instrumental": "",
			"altInstrumentals": []
		},
		"stage": "mainStage",
		"noteStyle": "funkin",
		"ratings": {}
	},

	"timeFormat": "ms",
	"timeChanges": [],
	"generatedBy": "FNF Mod Converter"
}

BASE_CHART = {
	"version": "2.0.0",
	"scrollSpeed": {},
	"events": [],
	"notes": {},
	"generatedBy": "FNF Mod Converter"
}

CHARACTER = {
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

ANIMATION = {
	"name": None,
	"prefix": None,
	"offsets": [0, 0]
}

FILE_LOCS = {																							
    # Class		 		# Original File				# Result				
    'PACKJSON': 		['/pack.json',				'/_polymod_meta.json'],
    'PACKPNG': 			['/pack.png', 				'/_polymod_icon.png'],
    'CREDITSTXT': 		['/data/credits.txt', 		'/mod-credits.txt'],
    'CHARACTERASSETS': 	['/images/characters/',		'/shared/images/characters/'],
    'CHARACTERJSONS':	['/characters/',			'/data/characters/'],
    'CHARACTERICON':	['/images/icons/',			'/images/icons/'],
    'CHARTFOLDER':		['/data/',					'/data/songs/'],
    'SONGS':			['/songs/',					'/songs/']
}