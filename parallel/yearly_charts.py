from utilities.file.io import load_object
from graphs.chart import YearlyChart

def draw_chart():
    files = get_filenames()
    dumps = [load_object("temp/merged", file) for file in files]
    chart = YearlyChart(dumps)

    chart.draw_yearly_address_space("address-space.png")
    #chart.draw_yearly_mode_allocated_block_size("mode-block-size.png")
    #chart.draw_yearly_mean_allocated_block_size("mean-block-size.png")

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
