import logging

from glob import glob
from pathlib import Path

def removeTrail(filename):
    return filename.replace('.json', '')

def findAll(folder):
    logging.info(f'Finding all files or directories with glob: {folder}')
    return glob(folder)

def folderMake(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        folder.mkdir(parents=True)