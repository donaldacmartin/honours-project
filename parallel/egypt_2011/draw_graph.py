from graphs.atlas.chrono_atlas_map import ChronoAtlasMap
from graphs.atlas.atlas_map import EGYPT
from pickle import load
from sys import argv

def draw_graph(file1, file2):
    parser1 = open_dump(file1)
    parser2 = open_dump(file2)

    c = ChronoAtlasMap(1920, 1080, parser1, parser1, EGYPT)
    c.save("finished_graphs/" + file1.replace("/", "_") + ".png")

def open_dump(filename):
    pickle_file = open("temp/merged/" + filename.replace("/", "_"), "rb")
    parser      = load(pickle_file)
    pickle_file.close()
    return parser

if __name__ == "__main__":
    draw_graph(argv[1], argv[2])
