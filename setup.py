import os
import pathlib
import shutil
import subprocess

#user inputs
inputPre=str(input("Input directory (Psych only for now): "))
outputPre=str(input("Output directory (Base Game only for now): "))

def detectEngine(inputEngineName, outputEngineName):
    print("Detected input engine:", inputEngineName)
    print("Detected output engine:", outputEngineName)

#Programmer writes worst code ever, asked to kill himself 🗣️⁉️
#i tried a match case earlier but it was fucking up. Ill go back to that later
if "PsychEngine" in inputPre and "CodenameEngine" in outputPre:
   detectEngine("Psych Engine", "Codename Engine")
elif "CodenameEngine" in inputPre and "PsychEngine" in outputPre:
    detectEngine("CodenameEngine", "PsychEngine")
elif "PsychEngine" in inputPre:
    detectEngine("Psych Engine", "Base Game")
elif "PsychEngine" in outputPre:
    detectEngine("Base Game", "Psych Engine")
else: detectEngine("Idk", "Idk")
#ok im killing myself now

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

import psychtobase.src.foldermoving