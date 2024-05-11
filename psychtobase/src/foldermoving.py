#You have to run setup.py first, this can't be run on its own
import shutil
from __main__ import *
import pathlib

#will redo this later the way tom was suggesting
folderStructure = {
    "Music": ("music", "music"),
    "Videos": ("videos", "videos"),
    "Songs": ("songs", "songs"),
    "Sounds": ("sounds", "sounds")
}

def copyFolder(inputFolder, outputFolder):
    #i need to think of variable names but i think im running out
    copytreeInput = pathlib.PurePath(inputDir , inputFolder)
    copytreeOutput = pathlib.PurePath(outputDir , outputFolder)
    try:
        shutil.copytree(copytreeInput, copytreeOutput)
        print("SUCCESS", copytreeInput, "copied to", copytreeOutput)
    except:
        print("ERROR", copytreeInput, "failed to copy to", copytreeOutput, "!")

print(inputDir)
print(outputDir)
for x in folderStructure.values():
    try:
        #again, this part will be redone
        copyFolder(x[0], x[1])
    except:
        print(x[0], "had a stroke trying to copy to", x[1])
