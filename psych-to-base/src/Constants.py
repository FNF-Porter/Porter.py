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