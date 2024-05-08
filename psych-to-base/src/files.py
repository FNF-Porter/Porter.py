import glob
import logging

def removeTrail(filename):
    return filename.replace('.json', '')

def findAll(folder):
    # return all files inside of a directory
    # currently only used by the main
    # update this!
    logging.info(f'Finding all files in {folder}')
    return glob.glob(folder)