from src import log, files, window
from src.convert import character as chars

# Main

def convert(psych_mod_folder, result_folder, options):
    log.trace('main.py', 'Converting started...')
    print(psych_mod_folder, result_folder, options)

    if options['characters']:
        for character in files.findAll('', ''):
            print(chars.character_convert(character))

    done_converting()

def done_converting():
    log.trace('main.py', 'Conversion done.')
    log.save()

def main():
    log.trace('main.py', 'Logging started...')
    window.init()

if __name__ == '__main__':
    main()