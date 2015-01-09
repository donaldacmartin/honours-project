#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from pickle import load, dump

"""
IO

Some functions to help save Python objects to files between operations carried
out by GNU Parallel.
"""

def save_object(directory, filename, obj):
    safe_filename = _create_safe_filename(filename)
    file = open(directory + "/" + safe_filename, "wb")
    dump(file, obj)
    file.close()

def load_object(directory, filename, obj):
    safe_filename = _create_safe_filename(filename)
    file = open(directory + "/" + safe_filename, "rb")
    obj  = load(file)
    file.close()
    return obj

def _create_safe_filename(filename):
    filename = filename.replace("/", "_")
    filename = filename.replace("\\", "_")
    filename = filename.replace("|", "_")
    return filename
