import json
import logging
import os
import shutil
from src import Constants
from src.tools import ModConvertTools as ModTools

from src import log, files, window
from src.tools.CharacterTools import CharacterObject
from src.tools.ChartTools import ChartObject

# Main

def folderMake(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def fileCopy(source, destination):
    shutil.copyfile(source, destination)

def convert(psych_mod_folder, result_folder, options):
    logging.info('Converting started...')
    logging.info(options)

    modfolder = 'WeekEnd1'
    result_folder = 'output'

    if options.get('modpack_meta', False):
        logging.info('Converting pack.json')

        dir = Constants.FILE_LOCS.get('PACKJSON')
        psychPackJson = dir[0]
        polymodMetaDir = dir[1]
        
        if os.path.exists(f'{modfolder}{psychPackJson}'):
            polymod_meta = ModTools.convertPack(json.loads(open(f'{modfolder}{psychPackJson}', 'r').read()))
            folderMake(f'{result_folder}/mod/')
            open(f'{result_folder}/mod/{polymodMetaDir}', 'w').write(json.dumps(polymod_meta, indent=4))

            logging.info('pack.json converted and saved')
        else:
            logging.warn('pack.json not found. Skipped')

        logging.info('Copying pack.png')
        dir = Constants.FILE_LOCS.get('PACKPNG')
        psychPackPng = dir[0]
        polymodIcon = dir[1]
        
        if os.path.exists(f'{modfolder}{psychPackPng}'):
            folderMake(f'{result_folder}/mod/')
            try:
                fileCopy(f'{modfolder}{psychPackPng}', f'{result_folder}/mod/{polymodIcon}')
            except:
                logging.error('Could not copy pack.png file')
        else:
            logging.warn('pack.png not found. Skipped')

        logging.info('Converting data/credits.txt')
        dir = Constants.FILE_LOCS.get('CREDITSTXT')

        psychCredits = dir[0]
        modCredits = dir[1]

        if os.path.exists(f'{modfolder}{psychCredits}'):
            folderMake(f'{result_folder}/mod/')
            resultCredits = ModTools.convertCredits(open(f'{modfolder}{psychCredits}', 'r').read())
            open(f'{result_folder}/mod/{modCredits}', 'w').write(resultCredits)
        else:
            logging.warn('Could not find data/credits.txt')

    if options.get('charts', False):
        folderMake(f'{result_folder}/mod/data/songs/')
        
        chartFolder = Constants.FILE_LOCS.get('CHARTFOLDER')
        psychChartFolder = modfolder + chartFolder[0]
        bgChartFolder = result_folder + '/mod' + chartFolder[1]
        songs = files.findAll(f'{psychChartFolder}*')

        for song in songs:
            logging.info(f'Checking if {song} is a valid chart directory...')
            if os.path.isdir(song):
                logging.info(f'Loading charts in {song}')

                songChart = ChartObject(song, psychChartFolder, bgChartFolder)
                
                logging.info(f'Converting charts of {song}...')
                songChart.convert()

                logging.info(f'{song} charts converted, saving')
                songChart.save()

    if options.get('characters', False):
        logging.info('Copying character assets...')

        dir = Constants.FILE_LOCS.get('CHARACTERASSETS')
        psychCharacterAssets = modfolder + dir[0]
        bgCharacterAssets = dir[1]

        folderMake(f'{result_folder}/mod/shared/images/characters/')

        for character in files.findAll(f'{psychCharacterAssets}*'):
            if not os.path.isdir(character):
                logging.info(f'Copying asset {character}')
                try:
                    fileCopy(character, result_folder + '/mod' + bgCharacterAssets + os.path.basename(character))
                except:
                    logging.error(f'Could not copy asset {character}!')
            else:
                logging.warn(f'{character} is a directory, not a file! Skipped')

        logging.info('Converting character jsons...')
        folderMake(f'{result_folder}/mod/data/characters/')

        dir = Constants.FILE_LOCS.get('CHARACTERJSONS')

        psychCharacters = modfolder + dir[0]
        bgCharacters = dir[1]

        for character in files.findAll(f'{psychCharacters}*'):
            logging.info(f'Checking if {character} is a file...')
            if not os.path.isdir(character) and character.endswith('.json'):
                converted_char = CharacterObject(character, result_folder + '/mod' + bgCharacters)

                converted_char.convert()
                converted_char.save()
            else:
                logging.warn(f'{character} is a directory, or not a json! Skipped')


    done_converting()

def done_converting():
    logging.info('Conversion done.')

def main():
    log.setup()
    window.init()

if __name__ == '__main__':
    main()