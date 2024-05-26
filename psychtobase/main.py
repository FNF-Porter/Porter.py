from base64 import b64decode
import json
import logging
import shutil
import time
from pathlib import Path
from PIL import Image
from src import Constants, log, Paths, Utils, files, window
from src.tools import ModConvertTools as ModTools
import threading

from src.tools.CharacterTools import CharacterObject
from src.tools.ChartTools import ChartObject
from src.tools import VocalSplit, WeekTools, StageTool, StageLuaParse
from src import Utils

if __name__ == '__main__':

    log.setup()
    window.init()

# Main

charts = []
characterMap = {
    # 'charactr': 'Name In English'
}
vocalSplitMasterToggle = True

def folderMake(folder_path):
    if not Path(folder_path).exists():
        try:
            Path(folder_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f'Something went wrong: {e}')

def fileCopy(source, destination):
    if Path(source).exists():
        try:
            shutil.copyfile(source, destination)
        except Exception as e:
            logging.error(f'Something went wrong: {e}')
    else:
        logging.warn(f'Path {source} doesn\'t exist.')

def treeCopy(source, destination):
    if not Path(destination).exists() and Path(source).exists():
        try:
            shutil.copytree(source, destination)
        except Exception as e:
            logging.error(f'Something went wrong: {e}')
    elif not Path(source).exists():
        logging.warn(f'Path {source} does not exist.')

def convert(psych_mod_folder, result_folder, options):
    runtime = time.time()

    logging.info(Utils.coolText("NEW CONVERSION STARTED"))

    logging.info('Converting started...')
    logging.info(options)

    modName = psych_mod_folder # MOD FOLDER PSYCH ENGINE
    modFoldername = Path(psych_mod_folder).name

    logging.info(f'Converting from{psych_mod_folder} to {result_folder}')

    if options.get('modpack_meta', False):
        logging.info('Converting pack.json')

        dir = Constants.FILE_LOCS.get('PACKJSON')
        psychPackJson = dir[0]
        polymodMetaDir = dir[1]
        
        if Path(f'{modName}{psychPackJson}').exists():
            polymod_meta = ModTools.convertPack(json.loads(open(f'{modName}{psychPackJson}', 'r').read()))
            folderMake(f'{result_folder}/{modFoldername}/')
            open(f'{result_folder}/{modFoldername}/{polymodMetaDir}', 'w').write(json.dumps(polymod_meta, indent=4))

            logging.info('pack.json converted and saved')
        else:
            folderMake(f'{result_folder}/{modFoldername}/')
            open(f'{result_folder}/{modFoldername}/{polymodMetaDir}', 'w').write(json.dumps(ModTools.defaultPolymodMeta(), indent=4))
            logging.warn('pack.json not found. Replaced it with default')

        logging.info('Copying pack.png')
        dir = Constants.FILE_LOCS.get('PACKPNG')
        psychPackPng = dir[0]
        polymodIcon = dir[1]
        
        if Path(f'{modName}{psychPackPng}').exists():
            folderMake(f'{result_folder}/{modFoldername}/')
            try:
                fileCopy(f'{modName}{psychPackPng}', f'{result_folder}/{modFoldername}/{polymodIcon}')
            except Exception as e:
                logging.error(f'Could not copy pack.png file: {e}')
        else:
            logging.warn('pack.png not found. Replacing it with default')
            try:
                _polyEncode = b'iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAYAAAA8AXHiAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsEAAA7BAbiRa+0AAAkcSURBVHhe7Z2xbhQ7GIXDfQwUURCegQJBCgrgAVIAFVWkUCNoKNOAqINERZUgxAMECgpAFDwDQRFCeY175zN79prRzCYz2ZOs2PNJlj0e2+OZOfPbWRv+C/82rIQwZ/6ZxCHMlQgrWIiwgoUIK1iIsIKFCCtYiLCChQgrWIiwgoUIK1iIsIKFCCtYiLCChQgrWIiwgoUIK1gYJawLFy6U8ObNm0nObx4+fFjy79y5M8k5nufPn5c6V65cmeSEk7Dozy0WK1iIsIIFq7AYKjVs/vjxY5om9PHly5dpGYbUIW3U5wgaqus2aQO6hhLS5FGea5NmeFdZHfeh+pTXtIBAe8f1XXUVaKOmvgfCwsM/phgK1Qh7e3uTnN9sbW2V/Nu3b5djzqtsO1AWnj17Vo7X1tbKMTHHQ9r4/Plz53mC+qhjygLtK+/g4KAE0upHfb4d1EYb9b0duvLVd123K/BsYNb9qb+LxpkNhc3DQcQrzQsrxx8+fChxDV9p86BLen9/v8Q1fW1sb2+XuHnI5TyheXEl7+nTpyVWna9fv5b4/fv3JYZv376tHB0dlfStW7dKLNSm+gVqow+uRZ1G1OWYuo1I/ui7LOeLFy9KDOo7ZeHJkycl7ro/tbOojBIWNziU69evl/jmzZslbsPD14NEQF30tfH9+/cS6wXA/fv3S0y7vETVOTw8LMMKSHw/f/6cimV9fb3EQkK7fPnyie9b11pdXS0xbGxslFjn1GcJTGIClQX62nV/Dx48mKQWk1NZLF5IF7yEodQvbXd3d5KaH9euXSsxVk4ievToUYk/fvxYBAdXr14tcTgdo4Slr1gWBviyXr58WdLtr/6kaOigHVmVk6AJuIY9kDgRLELH2pHGgiEkhhJZIYZFBKeyZ4muVz/Ld+/eTVK/rbTu7/Xr1yWG+l4XkVHC0pcO+ivlxo0b5ZiXc/fu3ZIeCvU0d1B7J0EPGdGoPxJ5PXzog0BIGpKUR93Nzc2SPku6nqVEpuFRwx79Vhn6u8iMEhZfGRPINohC84Gx7OzsTFL/W6Lj4KvuetDM1WqR15ZUQ2NX3lnS9yyx3o8fPy5p7qGeg/Gc6+NFJP93Q7Bwqsl7CH1EWMFChBUsRFjBQoQVLERYwUKEFSxEWMFChBUsRFjBQoQVLERYwUKEFSxEWMFChBUsRFjBQoQVLERYwUKEFSxEWMFChBUsRFjBQoQVLERYwUKEFSxEWMFChBUsRFjBQoQVLERYwUKEFSxEWMFChBUsRFjBQoQVLERYwUKEFSxEWMFChBUsRFjBQoQVLERYwcJoYbVdyRL+BvruRfc7xEP/MjNKWHhCxTsXjoJwxUNYJKdB8iM9xDVdmC+DhYVHUNye4YFK3qmgTp83nz59mqTCeTFYWHLSOMt1rDzAK8hyyJLUHtvlOk515HlenuPlzb3dJmh4UnuUwXu8fBViVeV1Xu0pqE/HeZdvg9u8ujz11baupTaXetjErdwQmiGveE+Xd/g2jSUr5/G8Xh8fHBxMPdKTB3VblCct7+51PaWBY7WhOjonaIM89UHX0fHaxKs81PX72oP2ubofQJp2QffZ94yWgbn/VYgXULysth2D4yleyF3tpUuXSoxvabnWlWd62mleWilLGrAClIHa4SblZoGrXsCC0YacZr59+7bEcjquPsxCZekXZdU38mkXSygXu2M9zf4NDBaWvJA65jG40eXlaDish1teYvMhTMMYT660Xbdx8eLFyZnTI6/5ODJHbBLgsjJYWHzVWAjmMRIAaH7BOV6g3P7LWpzEO7xejnw864tXm/W8qL52H79+/SqxrGbtxJt5kYQlK0n7XGcWmr+pbNvayZ+z7mVpab7cUTQPdDrnUBCNEP7Ib15Aydfcg7r1MXMg0bycP8oI5SvU8zKuV8P1VE7ttPvb7kM7tKnnWAr0qUZzuXb+MhKf0HMEK6bf9xbp55fzYO6T92Vmd3e3xMsuKoiw5oB+n2P+1QyZk9zlJkNhsBCLFSxEWMFChBUsjBIWE9U6tBeS9WOpqMvwJ3ldt6s81IvO+rEVtMBLUJtDUP1ZdTUZP811lp3RFotfmZn3E9rLK/x1pF/J+9ja2prW39nZmeR2U/9iXq85OkDk9+7dW9nb25v2b3Nzc3L2/KF/iH3RsQ2Fs7bVnBTES9CyELDAyxKPAz4GPgpEXy8gL9LvUlp+WnQswuKXZ9bRtJfqNLAwzaKuhkPSWvurae+3qq9dD78ItQ/9wDlrnY9hsb6O+iVLUp/XEN8uq2FeVl3nCdrDpftRexyT1lomeVovracNBNA9q77aPTMaUz8YqtVB625aI2StTmkg1vpZ15ob63VtVF/lWYfTup7y1KbW6IjrY8pr3VBl1YaOa7SeSPtdUIfztFkfg+qqD/WzqPsDpHV90pQF9Y3yqqNzor4m1M9Z90pe/ZzPg7nMsbrmSNqh0DUxh3qONWvfkvZ1MRyyVYfrtre7aKjc2Ngocb21R3MyzZPG7pHC2jQvrgzD2k+GNYV6Pqk9ZipzdHQ07Rf9UVn6ozRWGKvC3A4ODw9LDF3WuUb7wajPs4Ehe9Vc2OZYCALxaJvJaaAdHiDzC+dEen19vcTsqZon2hRI/9W2xAb1R9b3oc6i/sgJY/aqzRubsGDoA+pDcx4shqxRTXuXql4eQlldXS1pWbVZ+7iwZrwk9lTVVgir294xCppIy6rOgg+C/r969Wpq9VSv/vjon+Zis1AZ2qJd9Zf8Wfd4VliFBc28YZIaj14AL7brJfJXWzMnKUMJQwLC4LoIhfKcaw83ffC187K0jZkgAXGOPiifF4qFOAmyUNSp/2LmGNTmcf3b3t4uMf1AQPv7+yWt/pJeBLIIHSzYLVZYTiKsYCHCChYirGAhwgoWIqxgIcIKFiKsYCHCChYirGAhwgoWIqxgIcIKFiKsYCHCChYirGAhwgoWIqxgIcIKFiKsYCHCChYirGAhwgoWIqxgIcIKFiKsYCHCChYirGAhwgoWIqxgIcIKFiKsYCHCChYirGAhwgoWIqxgIcIKFiKsYCHCChYirGAhwgoWIqxgIcIKFiKsYCHCChYirGAhwgoWIqxgIcIKFiKsYCHCChYirGAhwgoGVlb+A3vagv0fYDEJAAAAAElFTkSuQmCC'
                polymodIconpath = f'{result_folder}/{modFoldername}/{polymodIcon}'
                with open(polymodIconpath, 'wb') as output_file:
                    #cause the image wasnt working in the executable
                    output_file.write(b64decode(_polyEncode))
            except Exception as e:
                logging.error(f'Could not write default file: {e}')

        logging.info('Parsing and converting credits.txt')
        dir = Constants.FILE_LOCS.get('CREDITSTXT')

        psychCredits = dir[0]
        modCredits = dir[1]

        if Path(f'{modName}{psychCredits}').exists():
            folderMake(f'{result_folder}/{modFoldername}/')
            resultCredits = ModTools.convertCredits(open(f'{modName}{psychCredits}', 'r').read())
            open(f'{result_folder}/{modFoldername}/{modCredits}', 'w').write(resultCredits)
        else:
            logging.warn(f'Could not find {modName}{psychCredits}')

    if options.get('charts', False):
        
        chartFolder = Constants.FILE_LOCS.get('CHARTFOLDER')
        psychChartFolder = modName + chartFolder[0]

        folderMake(f'{result_folder}/{modFoldername}{chartFolder[1]}')

        songs = files.findAll(f'{psychChartFolder}*')

        for song in songs:
            logging.info(f'Checking if {song} is a valid chart directory...')
            if Path(song).is_dir():
                logging.info(f'Loading charts in {song}')

                outputpath = f'{result_folder}/{modFoldername}'

                try:
                    songChart = ChartObject(song, outputpath)
                except FileNotFoundError:
                    logging.warning(f"{song} data not found! Skipping...")
                    continue
                except Exception as e:
                    logging.warning("ERROR!" + e)
                    continue
                else:
                    logging.info(f'{song} successfully initialized! Converting')

                songChart.convert()

                songName = songChart.songNameRaw
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
        psychCharacterAssets = modName + dir[0]
        bgCharacterAssets = dir[1]

        folderMake(f'{result_folder}/{modFoldername}{bgCharacterAssets}')

        for character in files.findAll(f'{psychCharacterAssets}*'):
            if Path(character).is_file():
                logging.info(f'Copying asset {character}')
                try:
                    fileCopy(character, result_folder + f'/{modFoldername}' + bgCharacterAssets + Path(character).name)
                except Exception as e:
                    logging.error(f'Could not copy asset {character}: {e}')
            else:
                logging.warn(f'{character} is a directory, not a file! Skipped')

    if options.get('characters', {
            'json': False
        })['json']:

        logging.info('Converting character jsons...')

        dir = Constants.FILE_LOCS.get('CHARACTERJSONS')

        psychCharacters = modName + dir[0]
        bgCharacters = dir[1]

        folderMake(f'{result_folder}/{modFoldername}{bgCharacters}')

        for character in files.findAll(f'{psychCharacters}*'):
            logging.info(f'Checking if {character} is a file...')
            if Path(character).is_file() and character.endswith('.json'):
                converted_char = CharacterObject(character, result_folder + f'/{modFoldername}' + bgCharacters)

                converted_char.convert()
                converted_char.save()

                # For THOSE
                fileBasename = converted_char.iconID.replace('icon-', '')
                if fileBasename in characterMap:
                    characterMap[fileBasename].append(converted_char.characterName)
                else:
                    characterMap[fileBasename] = [converted_char.characterName]
                logging.info(f'Saved {converted_char.characterName} to character map using their icon id: {fileBasename}.')
            else:
                logging.warn(f'{character} is a directory, or not a json! Skipped')

    if options.get('characters', {
        'icons': False
    })['icons']:
        logging.info('Copying character icons...')

        dir = Constants.FILE_LOCS.get('CHARACTERICON')
        psychCharacterAssets = modName + dir[0]
        bgCharacterAssets = dir[1]
        freeplayDir = Constants.FILE_LOCS.get('FREEPLAYICON')[1]

        folderMake(f'{result_folder}/{modFoldername}{bgCharacterAssets}')
        folderMake(f'{result_folder}/{modFoldername}{freeplayDir}')

        for character in files.findAll(f'{psychCharacterAssets}*'):
            if Path(character).is_file():
                logging.info(f'Copying asset {character}')
                try:
                    filename = Path(character).name
                    # Some goofy ah mods don't name icons with icon-, causing them to be invalid in base game.
                    if not filename.startswith('icon-') and filename != 'readme.txt':
                        logging.warn(f"Invalid icon name being renamed from '{filename}' to 'icon-{filename}'!")
                        filename = 'icon-' + filename
                    
                    destination = f'{result_folder}/{modFoldername}{bgCharacterAssets}{filename}'
                    fileCopy(character, destination)
                    keyForThisIcon = filename.replace('icon-', '').replace('.png', '')
                    logging.info('Checking if ' + keyForThisIcon + ' is in the characterMap')

                    if keyForThisIcon in characterMap:
                        try:
                            # Woah, freeplay icons
                            logging.getLogger('PIL').setLevel(logging.INFO)
                            with Image.open(character) as img:
                                # Get the winning/normal half of icons
                                normal_half = img.crop((0, 0, 150, 150))
                                # Scale to 50x50, same size as BF and GF pixel icons
                                pixel_img = normal_half.resize((50, 50), Image.Resampling.NEAREST)

                                for characterName in characterMap[keyForThisIcon]:
                                    pixel_name = characterName + 'pixel.png'
                                    freeplay_destination = f'{result_folder}/{modFoldername}{freeplayDir}/{pixel_name}'
                                    pixel_img.save(freeplay_destination)
                                    logging.info(f'Saving converted freeplay icon to {freeplay_destination}')
                        except Exception as ___exc:
                            logging.error(f"Failed to create character {keyForThisIcon}'s freeplay icon: {___exc}")
                except Exception as e:
                    logging.error(f'Could not copy asset {character}: {e}')
            else:
                logging.warn(f'{character} is a directory, not a file! Skipped')

    songOptions = options.get('songs', {
        'inst': False,
        'voices': False,
        'split': False,
        'sounds': False,
        'music': False
    })
    if songOptions:
        dir = Constants.FILE_LOCS.get('SONGS')
        psychSongs = modName + dir[0]
        bgSongs = dir[1]

        folderMake(f'{result_folder}/{modFoldername}{bgSongs}')

        _allSongFiles = files.findAll(f'{psychSongs}*')

        for song in _allSongFiles:
            _songKeyUnformatted = Path(song).name
            songKeyFormatted = _songKeyUnformatted.replace(' ', '-').lower()

            _allSongFilesClear = [Path(__song).name for __song in _allSongFiles]
            isPsych073Song =  'Voices-Opponent.ogg' in _allSongFilesClear and 'Voices-Player.ogg' in _allSongFilesClear

            logging.info(f'Checking if {song} is a valid song directory...')
            if Path(song).is_dir():
                logging.info(f'Copying files in {song}')
                for songFile in files.findAll(f'{song}/*'):
                    if Path(songFile).name == 'Inst.ogg' and songOptions['inst']:
                        logging.info(f'Copying asset {songFile}')
                        try:
                            folderMake(f'{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}')
                            fileCopy(songFile,
                              f'{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}/{Path(songFile).name}')
                        except Exception as e:
                            logging.error(f'Could not copy asset {songFile}: {e}')
                    elif Path(songFile).name == 'Voices.ogg' and songOptions['split'] and vocalSplitMasterToggle and not isPsych073Song:
                        # Vocal Split
                        songKey = _songKeyUnformatted

                        chart = None
                        for _chart in charts:
                            if _chart['songKey'] == songKey:
                                chart = charts[charts.index(_chart)]

                        if chart != None:
                            sections = chart['sections']
                            bpm = chart['bpm']
                            logging.info(f'Vocal Split ({songKey}) BPM is {bpm}')
                            path = song + '/'
                            resultPath = result_folder + f'/{modFoldername}{bgSongs}{songKeyFormatted}/'
                            songChars = [chart['player'],
                                          chart['opponent']]
                            
                            #print(songChars)

                            logging.info(f'Vocal Split currently running for: {songKey}')
                            logging.info(f'Passed the following paths: {path} || {resultPath}')
                            logging.info(f'Passed characters: {songChars}')

                            vocal_split_thread = threading.Thread(target=VocalSplit.vocalsplit, args=(sections, bpm, path, resultPath, songKey, songChars))
                            vocal_split_thread.start()
                            vocal_split_thread.join()
                        else:
                            logging.warn(f'No chart was found for {songKey} so the vocal file will be copied instead.')
                            try:
                                folderMake(f'{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}')
                                fileCopy(songFile,
                                f'{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}/{Path(songFile).name}')
                            except Exception as e:
                                logging.error(f'Could not copy asset {songFile}: {e}')
                    elif isPsych073Song:
                        songKey = _songKeyUnformatted

                        folderMake(f'{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}')

                        chart = None
                        for _chart in charts:
                            if _chart['songKey'] == songKey:
                                chart = charts[charts.index(_chart)]

                        if chart != None:
                            try:
                                if Path(songFile).name == 'Voices-Player.ogg':
                                    fileCopy(songFile, f"{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}/Voices-{chart.metadata['playData']['characters'].get('player')}.ogg")
                                elif Path(songFile).name == 'Voices-Opponent.ogg':
                                    fileCopy(songFile, f"{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}/Voices-{chart.metadata['playData']['characters'].get('opponent')}.ogg")

                            except Exception as e:
                                logging.error(f'Could not copy asset {songFile}: {e}')
                        else:
                            logging.warning(f'{songKeyFormatted} is a Psych Engine 0.7.3 song with separated vocals. Copy rename was attempted, however your chart was not found. These files will be copied instead.')
                            ## Psst! If you were taken here, your chart is needed to set your character to the file!
                            fileCopy(songFile,
                              f'{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}/{Path(songFile).name}')

                    elif songOptions['voices']:
                        logging.info(f'Copying asset {songFile}')
                        if not vocalSplitMasterToggle:
                            logging.warning('Vocal Split is disabled! This copy is the last.')

                        try:
                            folderMake(f'{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}')
                            fileCopy(songFile,
                              f'{result_folder}/{modFoldername}{bgSongs}{songKeyFormatted}/{Path(songFile).name}')
                        except Exception as e:
                            logging.error(f'Could not copy asset {songFile}: {e}')
            # End block for 'songs' folder

            if songOptions['sounds']: # Some people use directories on sounds, so I am adding support
                sounds_dir = Constants.FILE_LOCS.get('SOUNDS')
                psychSounds = modName + sounds_dir[0]
                baseSounds = sounds_dir[1]

                # Thankfully, glob ignores folders or files if they do not exist
                allsoundsindirsounds = files.findAll(f'{psychSounds}*')
                for asset in allsoundsindirsounds:
                    logging.info(f'Checking on {asset}')

                    if Path(asset).is_dir():
                        folderName = Path(asset).name
                        logging.info(f'{asset} is a tree, attempting to copy it')
                        try:
                            pathTo = f'{result_folder}/{modFoldername}{baseSounds}{folderName}'
                            treeCopy(asset, pathTo)
                        except Exception as e:
                            logging.error(f'Failed to copy {asset}: {e}')

                    else:
                        logging.info(f'{asset} is file, copying')
                        try:
                            folderMake(f'{result_folder}/{modFoldername}{baseSounds}')
                            fileCopy(asset, f'{result_folder}/{modFoldername}{baseSounds}{Path(asset).name}')
                        except Exception as e:
                            logging.error(f'Failed to copy {asset}: {e}')

            if songOptions['music']:
                sounds_dir = Constants.FILE_LOCS.get('MUSIC')
                psychSounds = modName + sounds_dir[0]
                baseSounds = sounds_dir[1]

                allsoundsindirsounds = files.findAll(f'{psychSounds}*')
            
                for asset in allsoundsindirsounds:
                    logging.info(f'Copying asset {asset}')
                    try:
                        folderMake(f'{result_folder}/{modFoldername}{baseSounds}')
                        fileCopy(asset,
                            f'{result_folder}/{modFoldername}{baseSounds}{Path(asset).name}')
                    except Exception as e:
                        logging.error(f'Could not copy asset {asset}: {e}')

    weekCOptions = options.get('weeks', {
            'props': False, # Asset
            'levels': False,
            'titles': False # Asset
        })  
    if weekCOptions['levels']:
        logging.info('Converting weeks (levels)...')

        dir = Constants.FILE_LOCS.get('WEEKS')
        psychWeeks = modName + dir[0]
        baseLevels = dir[1]

        folderMake(f'{result_folder}/{modFoldername}{baseLevels}')

        for week in files.findAll(f'{psychWeeks}*.json'):
            logging.info(f'Loading {week} into the converter...')

            weekJSON = json.loads(open(week, 'r').read())
            week_filename = Path(week).name
            converted_week = WeekTools.convert(weekJSON, modName, week_filename)
            open(f'{result_folder}/{modFoldername}{baseLevels}{week_filename}', 'w').write(json.dumps(converted_week, indent=4))

    if weekCOptions['props']:
        logging.info('Copying prop assets...')

        dir = Constants.FILE_LOCS.get('WEEKCHARACTERASSET')
        psychWeeks = modName + dir[0]
        baseLevels = dir[1]

        allXml = files.findAll(f'{psychWeeks}*.xml')
        allPng = files.findAll(f'{psychWeeks}*.png')
        for asset in allXml + allPng:
            logging.info(f'Copying {asset}')
            try:
                folderMake(f'{result_folder}/{modFoldername}{baseLevels}')
                fileCopy(asset,
                    f'{result_folder}/{modFoldername}{baseLevels}{Path(asset).name}')
            except Exception as e:
                logging.error(f'Could not copy asset {asset}: {e}')

    if weekCOptions['titles']:
        logging.info('Copying level titles...')

        dir = Constants.FILE_LOCS.get('WEEKIMAGE')
        psychWeeks = modName + dir[0]
        baseLevels = dir[1]

        allPng = files.findAll(f'{psychWeeks}*.png')
        for asset in allPng:
            logging.info(f'Copying {asset}')
            try:
                folderMake(f'{result_folder}/{modFoldername}{baseLevels}')
                fileCopy(asset,
                    f'{result_folder}/{modFoldername}{baseLevels}{Path(asset).name}')
            except Exception as e:
                logging.error(f'Could not copy asset {asset}: {e}')

    if options.get('stages', False):
        logging.info('Converting stages...')

        dir = Constants.FILE_LOCS.get('STAGE')
        psychStages = modName + dir[0]
        baseStages = dir[1]

        allStageJSON = files.findAll(f'{psychStages}*.json')
        for asset in allStageJSON:
            logging.info(f'Converting {asset}')
            folderMake(f'{result_folder}/{modFoldername}{baseStages}')
            stageJSON = json.loads(open(asset, 'r').read())
            assetPath = f'{result_folder}/{modFoldername}{baseStages}{Path(asset).name}'
        
            stageLua = asset.replace('.json', '.lua')
            logging.info(f'Parsing .lua with matching .json name: {stageLua}')

            luaProps = []
            if Path(stageLua).exists():
                logging.info(f'Parsing {stageLua} and attempting to extract methods and calls')
                try:
                    luaProps = StageLuaParse.parseStage(stageLua)
                except Exception as e:
                    logging.error(f'Could not complete parsing of {stageLua}: {e}')

            logging.info(f'Converting Stage JSON')
            stageJSONConverted = json.dumps(StageTool.convert(stageJSON, Path(asset).name, luaProps), indent=4)
            open(assetPath, 'w').write(stageJSONConverted)

    if options.get('images'): # Images include XMLs
        logging.info('Copying images')

        dir = Constants.FILE_LOCS.get('IMAGES')
        psychImages = modName + dir[0]
        baseImages = dir[1]

        allimagesandfolders = files.findAll(f'{psychImages}*')
        for asset in allimagesandfolders:
            logging.info(f'Checking on {asset}')

            if Path(asset).is_dir():
                logging.info(f'{asset} is directory, checking if it should be excluded...')
                folderName = Path(asset).name
                if not folderName in Constants.EXCLUDE_FOLDERS_IMAGES['PsychEngine']:
                    logging.info(f'{asset} is not excluded... attempting to copy.')
                    try:
                        pathTo = f'{result_folder}/{modFoldername}{baseImages}{folderName}'
                        #logging.debug(pathTo)

                        #folderMake(f'{result_folder}/{modFoldername}{baseImages}{folderName}')
                        treeCopy(asset, pathTo)
                    except Exception as e:
                        logging.error(f'Failed to copy {asset}: {e}')
                else:
                    logging.warn(f'{asset} is excluded. Skipped')

            else:
                logging.info(f'{asset} is file, copying')
                try:
                    folderMake(f'{result_folder}/{modFoldername}{baseImages}')
                    fileCopy(asset, f'{result_folder}/{modFoldername}{baseImages}{Path(asset).name}')
                except Exception as e:
                    logging.error(f'Failed to copy {asset}: {e}')

    #convlen = Utils.getRuntime(runtime)
    logging.info(Utils.coolText("CONVERSION COMPLETED"))
    logging.info(f'Conversion done: Took {int(time.time() - runtime)}s')
