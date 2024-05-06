import window
import log
from convert import character as chars
import files

# Main

def convert(psych_mod_folder, result_folder, options):
    log.log_line('main.py', 'Converting started...')
    print(psych_mod_folder, result_folder, options)

    if options['characters']:
        for character in files.findAll('', ''):
            print(chars.character_convert(character))

    done_converting()

def done_converting():
    log.log_line('main.py', 'Conversion done.')
    log.save_log()

def main():
    log.log_line('main.py', 'Logging started...')
    window.init()

if __name__ == '__main__':
    main()