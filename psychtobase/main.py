import json
import logging
import os
import shutil
from src import Constants
from src.tools import ModConvertTools as ModTools

from src import log, files, window
from src.tools.CharacterTools import CharacterObject
from src.tools.ChartTools import ChartObject
from src.tools import VocalSplit, WeekTools, StageTool, StageLuaParse
from src import Utils

# Main

charts = []
vocalSplitEnabled = True

def folderMake(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def fileCopy(source, destination):
    shutil.copyfile(source, destination)

def convert(psych_mod_folder, result_folder, options):
    logging.info('Converting started...')
    logging.info(options)

    modfolder = 'vs-skippa-psychengine' # MOD FOLDER PSYCH ENGINE
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
            folderMake(f'{result_folder}/mod/')
            open(f'{result_folder}/mod/{polymodMetaDir}', 'w').write(json.dumps(ModTools.defaultPolymodMeta(), indent=4))
            logging.warn('pack.json not found. Replaced it with default')

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
            logging.warn('pack.png not found. Replacing it with default')
            try:
                fileCopy(ModTools.defaultPolymodIconPath(), f'{result_folder}/mod/{polymodIcon}')
            except:
                logging.error('Could not copy default file')

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
        
        chartFolder = Constants.FILE_LOCS.get('CHARTFOLDER')
        psychChartFolder = modfolder + chartFolder[0]

        folderMake(f'{result_folder}/mod{chartFolder[1]}')

        songs = files.findAll(f'{psychChartFolder}*')

        for song in songs:
            logging.info(f'Checking if {song} is a valid chart directory...')
            if os.path.isdir(song):
                logging.info(f'Loading charts in {song}')

                songChart = ChartObject(song)
                
                logging.info(f'Converting charts of {song}...')
                songChart.convert()

                songName = songChart.songName
                charts.append({
                    'songKey': songName,
                    'sections': songChart.sections,
                    'bpm': songChart.startingBpm,
                    'player': songChart.metadata['playData']['characters']['player'],
                    'opponent': songChart.metadata['playData']['characters']['opponent']
                })

                logging.info(f'{song} charts converted, saving')
                songChart.save()

    if options.get('characters', {
			'assets': False
		})['assets']:
        logging.info('Copying character assets...')

        dir = Constants.FILE_LOCS.get('CHARACTERASSETS')
        psychCharacterAssets = modfolder + dir[0]
        bgCharacterAssets = dir[1]

        folderMake(f'{result_folder}/mod{bgCharacterAssets}')

        for character in files.findAll(f'{psychCharacterAssets}*'):
            if not os.path.isdir(character):
                logging.info(f'Copying asset {character}')
                try:
                    fileCopy(character, result_folder + '/mod' + bgCharacterAssets + os.path.basename(character))
                except:
                    logging.error(f'Could not copy asset {character}!')
            else:
                logging.warn(f'{character} is a directory, not a file! Skipped')

    if options.get('characters', {
			'json': False
		})['json']:

        logging.info('Converting character jsons...')

        dir = Constants.FILE_LOCS.get('CHARACTERJSONS')

        psychCharacters = modfolder + dir[0]
        bgCharacters = dir[1]

        folderMake(f'{result_folder}/mod{bgCharacters}')

        for character in files.findAll(f'{psychCharacters}*'):
            logging.info(f'Checking if {character} is a file...')
            if not os.path.isdir(character) and character.endswith('.json'):
                converted_char = CharacterObject(character, result_folder + '/mod' + bgCharacters)

                converted_char.convert()
                converted_char.save()
            else:
                logging.warn(f'{character} is a directory, or not a json! Skipped')

    if options.get('characters', {
		'icons': False
	})['icons']:
        logging.info('Copying character icons...')

        dir = Constants.FILE_LOCS.get('CHARACTERICON')
        psychCharacterAssets = modfolder + dir[0]
        bgCharacterAssets = dir[1]

        folderMake(f'{result_folder}/mod{bgCharacterAssets}')

        for character in files.findAll(f'{psychCharacterAssets}*'):
            if not os.path.isdir(character):
                logging.info(f'Copying asset {character}')
                try:
                    fileCopy(character, result_folder + '/mod' + bgCharacterAssets + os.path.basename(character))
                except:
                    logging.error(f'Could not copy asset {character}!')
            else:
                logging.warn(f'{character} is a directory, not a file! Skipped')

    songOptions = options.get('songs', {
        'inst': False,
        'voices': False,
        'split': False
    })
    if songOptions:
        dir = Constants.FILE_LOCS.get('SONGS')
        psychSongs = modfolder + dir[0]
        bgSongs = dir[1]

        folderMake(f'{result_folder}/mod{bgSongs}')

        for song in files.findAll(f'{psychSongs}*'):
            logging.info(f'Checking if {song} is a valid song directory...')
            if os.path.isdir(song):
                logging.info(f'Copying files in {song}')
                for songFile in files.findAll(f'{song}/*'):
                    if os.path.basename(songFile) == 'Inst.ogg' and songOptions['inst']:
                        logging.info(f'Copying asset {songFile}')
                        try:
                            folderMake(f'{result_folder}/mod{bgSongs}{os.path.basename(song)}')
                            fileCopy(songFile,
                              f'{result_folder}/mod{bgSongs}{os.path.basename(song)}/{os.path.basename(songFile)}')
                        except:
                            logging.error(f'Could not copy asset {songFile}!')
                    elif os.path.basename(songFile) == 'Voices.ogg' and songOptions['split'] and vocalSplitEnabled:
                        # Vocal Split
                        songKey = os.path.basename(song)

                        chart = None
                        for _chart in charts:
                            if _chart['songKey'] == songKey:
                                chart = charts[charts.index(_chart)]

                        if chart != None:
                            sections = chart['sections']
                            bpm = chart['bpm']
                            logging.info(f'Vocal Split ({songKey}) BPM is {bpm}')
                            path = song + '/'
                            resultPath = result_folder + f'/mod{bgSongs}{songKey}/'
                            songChars = [chart['player'],
                                          chart['opponent']]
                            
                            #print(songChars)

                            logging.info(f'Vocal Split currently running for: {songKey}')
                            logging.info(f'Passed the following paths: {path} || {resultPath}')
                            logging.info(f'Passed characters: {songChars}')

                            VocalSplit.vocalsplit(sections, bpm, path, resultPath, songKey, songChars)
                        else:
                            logging.warn(f'No chart was found for {songKey} so the vocal file will be copied instead.')
                            try:
                                folderMake(f'{result_folder}/mod{bgSongs}{os.path.basename(song)}')
                                fileCopy(songFile,
                                f'{result_folder}/mod{bgSongs}{os.path.basename(song)}/{os.path.basename(songFile)}')
                            except:
                                logging.error(f'Could not copy asset {songFile}!')
                    elif songOptions['voices']:
                        logging.info(f'Copying asset {songFile}')
                        try:
                            folderMake(f'{result_folder}/mod{bgSongs}{os.path.basename(song)}')
                            fileCopy(songFile,
                              f'{result_folder}/mod{bgSongs}{os.path.basename(song)}/{os.path.basename(songFile)}')
                        except:
                            logging.error(f'Could not copy asset {songFile}!')
    weekCOptions = options.get('weeks', {
			'props': False, # Asset
			'levels': False,
			'titles': False # Asset
		})  
    if weekCOptions['levels']:
        logging.info('Converting weeks (levels)...')

        dir = Constants.FILE_LOCS.get('WEEKS')
        psychWeeks = modfolder + dir[0]
        baseLevels = dir[1]

        folderMake(f'{result_folder}/mod{baseLevels}')

        for week in files.findAll(f'{psychWeeks}*.json'):
            logging.info(f'Loading {week} into the converter...')

            weekJSON = json.loads(open(week, 'r').read())
            open(f'{result_folder}/mod{baseLevels}{os.path.basename(week)}', 'w').write(json.dumps(WeekTools.convert(weekJSON, modfolder), indent=4))

    if weekCOptions['props']:
        logging.info('Copying prop assets...')

        dir = Constants.FILE_LOCS.get('WEEKCHARACTERASSET')
        psychWeeks = modfolder + dir[0]
        baseLevels = dir[1]

        allXml = files.findAll(f'{psychWeeks}*.xml')
        allPng = files.findAll(f'{psychWeeks}*.png')
        for asset in allXml + allPng:
            logging.info(f'Copying {asset}')
            try:
                folderMake(f'{result_folder}/mod{baseLevels}')
                fileCopy(asset,
                    f'{result_folder}/mod{baseLevels}{os.path.basename(asset)}')
            except:
                logging.error(f'Could not copy asset {asset}!')

    if weekCOptions['titles']:
        logging.info('Copying level titles...')

        dir = Constants.FILE_LOCS.get('WEEKIMAGE')
        psychWeeks = modfolder + dir[0]
        baseLevels = dir[1]

        allPng = files.findAll(f'{psychWeeks}*.png')
        for asset in allPng:
            logging.info(f'Copying {asset}')
            try:
                folderMake(f'{result_folder}/mod{baseLevels}')
                fileCopy(asset,
                    f'{result_folder}/mod{baseLevels}{os.path.basename(asset)}')
            except:
                logging.error(f'Could not copy asset {asset}!')

    if options.get('stages', False):
        logging.info('Converting stages...') # Todo make lua parsing and copy props as well

        dir = Constants.FILE_LOCS.get('STAGE')
        psychStages = modfolder + dir[0]
        baseStages = dir[1]

        allStageJSON = files.findAll(f'{psychStages}*.json')
        for asset in allStageJSON:
            logging.info(f'Converting {asset}')
            folderMake(f'{result_folder}/mod{baseStages}')
            stageJSON = json.loads(open(asset, 'r').read())
            assetPath = f'{result_folder}/mod{baseStages}{os.path.basename(asset)}'
        
            stageLua = asset.replace('.json', '.lua')
            logging.info(f'Parsing .lua with matching .json name: {stageLua}')

            luaProps = []
            if os.path.exists(stageLua):
                logging.info(f'Parsing {stageLua} and attempting to extract methods and calls')
                try:
                    luaProps = StageLuaParse.parseStage(stageLua)
                except Exception as e:
                    logging.error(f'Could not complete parsing of {stageLua}: {e}')

            logging.info(f'Converting Stage JSON')
            stageJSONConverted = json.dumps(StageTool.convert(stageJSON, os.path.basename(asset), luaProps), indent=4)
            open(assetPath, 'w').write(stageJSONConverted)

    runtime = Utils.getRuntime()
    logging.info(f'Conversion done: Took {int(runtime)}s')

if __name__ == '__main__':
    log.setup()
    window.init()