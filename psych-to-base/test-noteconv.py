# USED FOR TESTING CHART CONVERSION
# PHEW! SO FAR SO GOOD!

import os, logging
from src import log
from src.tools.ChartTools import ChartObject

if __name__ == "__main__":

	log.setup()

	songPath = "lit-up"

	abspath = os.path.dirname(os.path.abspath(__file__))
	os.chdir(abspath)

	try: os.makedirs(os.path.join("output", songPath))
	except Exception as e: logging.warning(e)

	chart = ChartObject(songPath)
	chart.convert()
	chart.save()