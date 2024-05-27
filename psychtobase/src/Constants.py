"""
A module full of templates needed for mod conversion.
"""

DEFAULT_OPTIONS = {
  'charts': False,
  'songs': { # Technically "audios", but whatever
    'inst': False,
    'voices': False,
    'split': False,
    'music': False,
    'sounds': False
  },
  'characters': {
    'icons': False,
    'json': False,
    'assets': False
  },
  'weeks': {
    'props': False,
    'levels': False,
    'titles': False
  },
  'stages': False,
  'modpack_meta': False,
  'images': False
}

DIFFICULTIES:list = ["easy", "normal", "hard"]

STAGES = {
	"stage": "mainStage"
}

CHARACTERS = {
	"pico-player": "pico-playable"
}

## templates begin here

BASE_CHART_METADATA = {
	"version": "2.2.0",
	"songName": "",
	"artist": "",
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
	"generatedBy": "FNF Porter (by Gusborg, tposejank, BombasticTom & VocalFan)"
}

BASE_CHART = {
	"version": "2.0.0",
	"scrollSpeed": {},
	"events": [],
	"notes": {},
	"generatedBy": "FNF Porter (by Gusborg, tposejank, BombasticTom & VocalFan)"
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
	"offsets": [0, 0],
  "frameRate": 24,
  "frameIndices": []
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
		},
    "dad": {
      "assetPath": "storymenu/props/dad",
      "scale": 1.0,
      "offsets": [100, 60],
      "animations": [
        {
          "name": "idle",
          "prefix": "idle0",
          "frameRate": 24
        }
      ]
    },
    "spooky": {
      "assetPath": "storymenu/props/spooky",
      "scale": 1.0,
      "offsets": [100, 120],
      "animations": [
        {
          "name": "danceLeft",
          "prefix": "idle0",
          "frameIndices": [0, 1, 2, 3, 4, 5, 6, 7]
        },
        {
          "name": "danceRight",
          "prefix": "idle0",
          "frameIndices": [8, 9, 10, 11, 12, 13, 14, 15]
        }
      ]
    },
    "pico": {
      "assetPath": "storymenu/props/pico",
      "scale": 1.0,
      "offsets": [100, 120],
      "animations": [
        {
          "name": "idle",
          "prefix": "idle0",
          "frameRate": 24
        }
      ]
    },
    "mom": {
      "assetPath": "storymenu/props/mom",
      "scale": 0.9,
      "offsets": [120, 50],
      "animations": [
        {
          "name": "idle",
          "prefix": "idle0",
          "frameRate": 24
        }
      ]
    },
    "parents-christmas": {
      "assetPath": "storymenu/props/parents-xmas",
      "scale": 0.9,
      "offsets": [10, 60],
      "animations": [
        {
          "name": "idle",
          "prefix": "idle0",
          "frameRate": 24
        }
      ]
    },
    "senpai": {
      "assetPath": "storymenu/props/senpai",
      "scale": 1.0,
      "offsets": [60, 100],
      "animations": [
        {
          "name": "idle",
          "prefix": "idle0",
          "frameRate": 24
        }
      ]
    },
    "tankman": {
      "assetPath": "storymenu/props/tankman",
      "scale": 1.0,
      "offsets": [100, 100],
      "animations": [
        {
          "name": "idle",
          "prefix": "idle0",
          "frameRate": 24
        }
      ]
    },
    "darnell": {
      "assetPath": "storymenu/props/darnell",
      "scale": 1.0,
      "offsets": [120, 120],
      "animations": [
        {
          "name": "idle",
          "prefix": "idle0",
          "frameRate": 24
        }
      ]
    },
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
    "animType": "multisparrow",
    "name": "peachscastle",
    "isPixel": False,
    "assetPath": None,
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

STAGE_PROP_ANIMATED = {
    "zIndex": None,
    "position": [0, 0],
    "scale": [1, 1],
    "animType": "sparrow",
    "name": "", # Psych Engine TAG
    "isPixel": False,
    "startingAnimation": "Idle",
    "assetPath": "stage assets/Road",
    "scroll": [1, 1],
    "animations": []
}

STAGE_PROP_ANIMATION = {
    "offsets": [0, 0],
    "flipY": False,
    "frameRate": 24,
    "prefix": None,
    "looped": True,
    "flipX": False,
    "name": None
}

STAGE_PROP_IMAGE = {
    "danceEvery": 0,
    "zIndex": None,
    "position": [0, 0],
    "scale": [1, 1],
    "name": None, # Psych Engine TAG
    "isPixel": False,
    "assetPath": None,
    "scroll": [1, 1]
}

## Folders which are IGNORED while copying images
## (They are either copied by another part of the code)
EXCLUDE_FOLDERS_IMAGES = {
    "PsychEngine": [
        'menubackgrounds',
        'icons',
        'dialogue',
        'storymenu',
        'menucharacters',
        'achievements',
        'credits',
        'characters',
        # 'mainmenu' I dont know how to override that yet
        # 'menudifficulties' Coming soon?
    ]
}

FILE_LOCS = {	# If the indent fucks up again its GitHub's fault
    # Class, psych directory, base game directory, codename directory (coming soon)			
    'PACKJSON':
    ['/pack.json',	'/_polymod_meta.json'],

    'PACKPNG': 
    ['/pack.png','/_polymod_icon.png'],

    'CREDITSTXT':
    ['/data/credits.txt','/mod-credits.txt'],

    'CHARACTERASSETS':
    ['/images/characters/',	'/shared/images/characters/'],

    'CHARACTERJSONS':
    ['/characters/', '/data/characters/'],

    'CHARACTERICON':
    ['/images/icons/','/images/icons/'],

    'CHARTFOLDER':
    ['/data/','/data/songs/'],

    'SONGS':
    ['/songs/','/songs/'],

    'SOUNDS':
    ['/sounds/', '/sounds/'],

    'MUSIC':
    ['/music/', '/music/'],

    'WEEKS':
    ['/weeks/','/data/levels/'],

    'WEEKCHARACTERASSET':
    ['/images/menucharacters/',		'/images/storymenu/props/'],

    'WEEKCHARACTERJSON': 
    ['/images/menucharacters/',	  ''], # Embedded directly to the level.json

    'WEEKIMAGE':
    ['/images/storymenu/','/images/storymenu/titles/'],

    'WEEKIMAGE_WEEKJSON':
    ['', 'storymenu/titles/'],

    'STAGE': 
    ['/stages/','/data/stages/'],

    'IMAGES':
    ['/images/','/shared/images/'],
    
    'FREEPLAYICON':
    ['/images/icons/','/images/freeplay/icons'],
}

VERSION = "0.2"