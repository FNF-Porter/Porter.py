# USED FOR TESTING CHART CONVERSION
# PHEW! SO FAR SO GOOD!

import os
from src.ChartTools import ChartObject

songPath = "lit-up"

abspath = os.path.dirname(os.path.abspath(__file__))
os.chdir(abspath)

try: os.makedirs(os.path.join("output", songPath))
except Exception as e: print("YO!", e)

chart = ChartObject(songPath)
chart.convert()
chart.save()