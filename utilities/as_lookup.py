class ASLookup(object):
    def __init__(self):
        table = self.load_file()

    def get_org_for_asys(self, asys):
        return table[asys]

    def load_file(self, filename="utilities/data/as_list.txt"):
        table = {}
        file  = open(filename, "r")
        line  = file.readline()[:-1]

        while line != "":
            table = self.parse_line(line, table)
            line  = file.readline()

        file.close()
        return table

    def parse_line(self, line, table):
        line = line.split("|")

        asys = line[0].strip()
        org  = line[1].strip()

        asys = int(asys)
        table[asys] = org
        return table
