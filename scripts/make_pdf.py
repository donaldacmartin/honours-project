from sys import argv

# Atlas Map -> (7016, 3947)
# Rest      -> (2338, 2338)

def organise_args():
    latex_template = argv[1]
    pdf_name       = argv[2]

def generate_atlas_map():
    command = ["scripts/plot_chart", "ATLAS_MAP", "01/06/2014", "7016x3947",
            "GLOBAL", "atlas.png"]

if __name__ == "__main__":
    getoutput("plot_chart")
