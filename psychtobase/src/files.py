from glob import glob
import logging
from os import path, makedirs

def removeTrail(filename):
    return filename.replace('.json', '')

def findAll(folder):
    # return all files inside of a directory
    # currently only used by the main
    # update this!
    logging.info(f'Finding all files or directories with glob: {folder}')
    return glob(folder)

def folderMake(folder_path): #Sorry Tom but I'm dumb and not patient!
    if not path.exists(folder_path):
        makedirs(folder_path)