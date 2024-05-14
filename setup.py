from pathlib import PurePath
import logging
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