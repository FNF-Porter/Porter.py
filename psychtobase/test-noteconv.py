# USED FOR TESTING CHART CONVERSION
# NOT THE FINAL PRODUCT

import os
from src import log
from src.tools.ChartTools import ChartObject

if __name__ == "__main__":

	log.setup()

	abspath = os.path.dirname(os.path.abspath(__file__))
	os.chdir(abspath)

	convSongs = ["darnell", "lit-up", "2hot"]

	for song in convSongs:
		chart = ChartObject(f"mods\{song}")
		chart.convert()
		chart.save()