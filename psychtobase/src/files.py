from glob import glob
import logging
from pathlib import Path

def removeTrail(filename):
    return filename.replace('.json', '')

def findAll(folder):
    # return all files inside of a directory
    # currently only used by the main
    # update this!
    logging.info(f'Finding all files or directories with glob: {folder}')
    return glob(folder)

def folderMake(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        folder.mkdir(parents=True)