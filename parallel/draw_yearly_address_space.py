from utilities.file.io import load_object
from graphs.chart.address_space import create_yearly_address_space

def draw_chart():
    filenames = get_filenames()
    dumps     = load_bgp_dumps(filenames)
    create_yearly_address_space(dumps)

def get_filenames():
    file  = open("temp/files_to_merge", "rb")
    names = []
    line  = file.readline()

    while line != "":
        filename = line.split("|")[0]
        names.append(filename)
        line = file.readline()

    file.close()
    return names

def load_bgp_dumps(files):
    dumps = []

    for file in files:
        dump = load_object("temp/merged", file)
        dumps.append(dump)

    return dumps
