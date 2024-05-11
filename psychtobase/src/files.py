import glob
import logging
import os

def removeTrail(filename):
    return filename.replace('.json', '')

def findAll(folder):
    # return all files inside of a directory
    # currently only used by the main
    # update this!
    logging.info(f'Finding all files in {folder}')
    return glob.glob(folder)

def folderMake(folder_path): #Sorry Tom but I'm dumb and not patient!
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)