from main import convert
import log

def init():
    log.log_line('window.py', 'Initiating window')

    # initiate the window

    # the code below should go on the callback when the person presses the convert button
    psych_mod_folder_path = 'path_after_user_selected_it'
    result_path = 'path_after_user_selected_it'
    options = {
        'shaders': True,
        'songs': False
    }

    if psych_mod_folder_path != None and result_path != None:
        convert(psych_mod_folder=psych_mod_folder_path, result_folder=result_path, options=options)

def report_progress(text):
    # update the bottom text to display text
    print(text)