# USED FOR TESTING CHART CONVERSION
# NOT THE FINAL PRODUCT

import os
from src import log
from src.tools.ChartTools import ChartObject

if __name__ == "__main__":

	log.setup()

	abspath = os.path.dirname(os.path.abspath(__file__))
	os.chdir(abspath)

	chart = ChartObject(f"mods\{input('YO! Which chart should I convert: ')}")
	chart.convert()
	chart.save()