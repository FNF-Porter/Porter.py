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

LEVEL_PROP_DEFAULTS = {
    "bf": {
            "assetPath": "storymenu/props/bf",
            "scale": 1.0,
            "offsets": [150, 80],
            "animations": [{
                    "name": "idle",
                    "prefix": "idle0",
                    "frameRate": 24
                },
                {
                    "name": "confirm",
                    "prefix": "confirm0",
                    "frameRate": 24
                }
            ]
        },
    "gf": {
            "assetPath": "storymenu/props/gf",
            "scale": 1.0,
            "offsets": [200, 80],
            "animations": [{
                    "name": "danceLeft",
                    "prefix": "idle0",
                    "frameIndices": [30, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                },
                {
                    "name": "danceRight",
                    "prefix": "idle0",
                    "frameIndices": [
                        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
                    ]
                }
            ]
		}
}

LEVEL_PROP = {
    "assetPath": None,
    "scale": None,
    "offsets": [],
    "animations": []
}

LEVEL_PROP_ANIMATION = {
    "name": None, # idle, confirm
    "prefix": None,
    "frameRate": 24
}

LEVEL = {
    "version": "1.0.0",
    "name": None,
    "titleAsset": None,
    "props": [],
    "background": None,
    "songs": []
}

STAGE_PROP = {
    "danceEvery": 0,
    "zIndex": 10,
    "position": [-600, -200],
    "scale": [1, 1],
    "animType": "sparrow",
    "name": "peachscastle",
    "isPixel": False,
    "assetPath": "stage assets/peachscastle/peachscastle",
    "scroll": [0.9, 0.9],
    "animations": []
}

STAGE = {
  "props": [],
  "cameraZoom": None,
  "version": "1.0.0",
  "characters": {
    "bf": {
      "zIndex": 300,
      "position": None,
      "cameraOffsets": [-100, -100]
    },
    "dad": {
      "zIndex": 200,
      "position": None,
      "cameraOffsets": [150, -100]
    },
    "gf": {
      "zIndex": 100,
      "cameraOffsets": [0, 50],
      "position": None
    }
  },
  "name": None
}

FILE_LOCS = {																							
    # Class		 			# Original File						# Result				
    'PACKJSON': 			['/pack.json',						'/_polymod_meta.json'],
    'PACKPNG': 				['/pack.png', 						'/_polymod_icon.png'],
    'CREDITSTXT': 			['/data/credits.txt', 				'/mod-credits.txt'],
    'CHARACTERASSETS': 		['/images/characters/',				'/shared/images/characters/'],
    'CHARACTERJSONS':		['/characters/',					'/data/characters/'],
    'CHARACTERICON':		['/images/icons/',					'/images/icons/'],
    'CHARTFOLDER':			['/data/',							'/data/songs/'],
    'SONGS':				['/songs/',							'/songs/'],
    'WEEKS':				['/weeks/',							'/data/levels/'],
    'WEEKCHARACTERASSET':	['/images/menucharacters/',			'/images/storymenu/props/'],
    'WEEKCHARACTERJSON':	['/images/menucharacters/',	''], # Embedded directly to the level.json
    'WEEKIMAGE':			['/images/storymenu/',				'/images/storymenu/titles/'],
    'STAGE':                ['/stages/',                        '/data/stages/']
}