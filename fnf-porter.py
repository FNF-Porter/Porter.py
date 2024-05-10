import os
import pathlib
import shutil

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

inputDir=str(pathlib.PurePath(inputPre , "mods" , modName))
outputDir=str(pathlib.PurePath(outputPre , "mods" , modName))
logDir=str(pathlib.PurePath(outputDir , "fnf-porter.log"))
print(inputDir)
print(outputDir)
print(logDir)

#The keys are nicknames
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
    shutil.copytree(copytreeInput, copytreeOutput)
    print("Attempted to copy", copytreeInput, "to", copytreeOutput)

for x in folderStructure.values():
    try:
        copyFolder(x[0], x[1])
    except:
        print(x[0], "had a stroke trying to copy to", x[1])
        #how do you get full path name

#call the converters in the appropriate folders