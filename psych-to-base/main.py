import logging

from src import log, files, window
from src.tools.CharacterTools import CharacterObject

# Main

def convert(psych_mod_folder, result_folder, options):
    logging.info('Converting started...')
    print(psych_mod_folder, result_folder, options)

    if options['characters']:
        for character in files.findAll('', ''):
            converted_char = CharacterObject(character)

            converted_char.convert()
            converted_char.save()

    done_converting()

def done_converting():
    logging.info('Conversion done.')

def main():
    log.setup()
    window.init()

if __name__ == '__main__':
    main()