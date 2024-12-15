import json
import logging
import shutil
import threading
import time

from base64 import b64decode
from pathlib import Path
from PIL import Image

from src import UI, Constants, FileContents, files, log, Utils

from src.tools import StageLuaParse, StageTool, VocalSplit, WeekTools
from src.tools import ModConvertTools as ModTools

from src.tools import CharacterTools
from src.tools import ChartTools 

from src.lua.Objects import LuaScript
from src.tools import StageTools

root = Path(__file__).parent

if __name__ == '__main__':
    log.setup()
    UI.init()