from utilities.file.io import load_object
from graphs.pyplot.pyplot_chart import YearlyChart
from graphs.ring import RingGraph
from graphs.chart.yearly_allocated_blocks import YearlyAllocatedBlocks
from graphs.atlas.standard import StandardAtlas

def draw_chart():
    files = get_filenames()
    dumps = [load_object("temp/merged", file) for file in files]

    generic_chart = YearlyChart(dumps)
    generic_chart.draw_address_space("address-space.png")
    generic_chart.draw_most_common_block_size("most-common-block-size.png")
    generic_chart.draw_stacked_allocation_of_blocks("stacked-allocation.png")

    y = YearlyAllocatedBlocks(dumps)
    y.save("yearly-blocks.png")

    s = StandardAtlas(dumps[-1])
    s.save("standard-atlas.png")

    r = RingGraph(dumps[-1])
    r.save("ring-graph.png")

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

if __name__ == "__main__":
    draw_chart()
