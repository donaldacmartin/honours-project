from sys import path
from os import remove
from logging import Formatter, StreamHolder, getLogger, DEBUG
def setup(python_path):
    path.append(python_path)

def setup_logger():
    formatter = Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler   = StreamHandler()
    handler.setFormatter(formatter)

    logger = getLogger(name)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)

def clean_up(temp_files):
    for file in temp_files:
        try:
            remove(file)
        except:
            print("Unable to remove file " + file)
