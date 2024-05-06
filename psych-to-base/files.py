import log

def removeTrail(filename):
    return filename.replace('.json', '')

def findAll(modPath, folder):
    # return all files inside of a directory
    # currently only used by the main
    # update this!
    log.log_line('files.py', f'Finding all files in {folder}')
    return ['senpai.json']