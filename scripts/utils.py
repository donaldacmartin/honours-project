from sys import path
from os import remove

def setup(python_path):
    path.append(python_path)

def clean_up(temp_files):
    for file in temp_files:
        try:
            remove(file)
        except:
            print("Unable to remove file " + file)
