from utilities.file.io import load_object
from graphs.chart import YearlyChart

def draw_chart():
    files = get_filenames()
    dumps = [load_object("temp/merged", file) for file in files]
    chart = YearlyChart(dumps)

    chart.draw_address_space("address-space.png")
    chart.draw_most_common_block_size("most-common-block-size.png")

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
