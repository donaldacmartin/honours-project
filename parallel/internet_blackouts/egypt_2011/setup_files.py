from utilities.file_search import FileBrowser

def create_list_of_files():
    root_dir = "/nas05/users/csp/routing-data/archive.routeviews.org"
    database = FileBrowser(root_dir)
    hourly   = []

    for dd in range(28, 29):
        files = database.get_files_for_time(2011, 1, dd, 0)
        hourly.append(files)

    """
    for dd in range(1, 4):
        files = database.get_files_for_time(2011, 2, dd, 0)
        hourly.append(files)
    """

    create_index_for_parallel_parsing(hourly)
    create_hours_for_merging(hourly)
    create_indices_for_creating_diff(hourly)

def create_index_for_parallel_parsing(hourly):
    output_file = open("temp/parsing_index", "wb")

    for hour in hourly:
        for router_file in hour:
            output_file.write(router_file + "\n")

    output_file.close()

def create_hours_for_merging(hourly):
    output_file = open("temp/merging_index", "wb")

    for hour in hourly:
        for router_file in hour:
            output_file.write(router_file + "|")
        output_file.write("\n")

    output_file.close()

def create_indices_for_creating_diff(hourly):
    files  = [hour[0] for hour in hourly]
    index1 = open("temp/diff_index_1", "wb")
    index2 = open("temp/diff_index_2", "wb")

    for i in range(1, len(files)):
        index1.write(files[i-1] + "\n")
        index2.write(files[i] + "\n")

    index1.close()
    index2.close()

if __name__ == "__main__":
    create_list_of_files()
