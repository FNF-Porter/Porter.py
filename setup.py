import os
import pathlib
import shutil
import logging
import datetime
from psychtobase import main
from psychtobase.src import log, window

def makePath(path, path2):
    return str(pathlib.PurePath(path, path2))

#def advanced was breaking it
#user inputs
def askMode():
    # lets rethink this for a moment
    modes = [
        'Psych Engine to Base Game',
        'Base Game to Psych Engine',
        'Codename to Psych Engine',
        'Psych Engine to Codename',
    ]

    for i, mode in enumerate(modes):
        print(f'{i + 1}: {mode}')

    mode = int(input("Conversion Mode (temporal): ")) - 1

    if mode < len(modes):
        print('Cool')
    else: logging.critical("Unknown Conversion Mode!")

if __name__ == '__main__':
    #Programmer writes worst code ever, asked to kill himself 🗣️⁉️
    #This is actually easier than a match case for some reason

    # _inputFolder = str(input("PsychEngine.exe mod directory (temporal): "))
    # _outputFolder = str(input("Funkin.exe mod directory (temporal): "))
    # _modFolder = '' # 'mods' when applicable

    # print("Your Mods:")
    # for mod in os.listdir(makePath(_inputFolder , _modFolder)):
    #     print(mod)

    # modName = input("Please specify the mod to convert (temporal): ")

    # askMode() # make use of this when doing other engine conversions

    log.setup()
    window.init()

    # match engineIn, engineOut:
    #     case "psych", "basegame":
    #         logging.info("Direction: Psych to Base Game")
    #         import psychtobase.src.main.py
    #         import psychtobase.src.foldermoving
    #     case "psych", "codename":
    #         print("Psych to Codename isn't supported yet!")
    #     case "basegame", "psych":
    #         print("Base Game to Psych isn't supported yet!")
    #     case __:
    #         print("uhh idk")