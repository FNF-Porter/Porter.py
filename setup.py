import os
import pathlib
import shutil
import logging
import datetime
from psychtobase import main
from psychtobase.src import log, window

#def advanced was breaking it
#user inputs
inputPre=str(input("Input directory (Psych only for now): "))
outputPre=str(input("Output directory (Base Game only for now): "))

#Programmer writes worst code ever, asked to kill himself 🗣️⁉️
#This is actually easier than a match case for some reason
def detectEngine(inputPre, outputPre):
    if "PsychEngine" in inputPre and "CodenameEngine" in outputPre:
        print("Psych to Codename isn't supported yet!")
        engineIn="psych"
        engineOut="codename"
    elif "CodenameEngine" in inputPre and "PsychEngine" in outputPre:
        print("Codename to Psych isnt supported yet!")
        engineIn="codename"
        engineOut="psych"
    elif "PsychEngine" in inputPre:
    #The folder name of the base game can be anything, so it just assumes its base game if its not psych or codename
        engineIn="psych"
        engineOut="basegame"
    elif "PsychEngine" in outputPre:
        engineIn="basegame"
        engineOut="psych"
    else: logging.critical("Unknown engine")
    print("Porting from", engineIn)
    print("To", engineOut)

detectEngine(inputPre, outputPre)

print("Your mods")
for a in os.listdir(pathlib.PurePath(inputPre , "mods")):
    print(a)
modName=str(input("Mod to port: "))
inputDir = str(pathlib.PurePath(inputPre , "mods" , modName))
outputDir = str(pathlib.PurePath(outputPre , "mods" , modName))
logDir = str(pathlib.PurePath(outputDir , "fnf-porter.log"))
print(inputDir)
print(outputDir)
print(logDir)

if __name__ == '__main__':
    log.setup()
    window.init()

match engineIn, engineOut:
    case "psych", "basegame":
        logging.info("Direction: Psych to Base Game")
        import psychtobase.src.main.py
        import psychtobase.src.foldermoving
    case "psych", "codename":
        print("Psych to Codename isn't supported yet!")
    case "basegame", "psych":
        print("Base Game to Psych isn't supported yet!")
    case __:
        print("uhh idk")
