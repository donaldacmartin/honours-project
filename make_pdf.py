from sys import argv
from subprocess import Popen

# Atlas Map -> (7016, 3947)
# Rest      -> (2338, 2338)

graph    = ["python", "scripts/plot_graph.py"]
chart    = ["python", "scripts/plot_chart.py"]
date     = ["01/06/2014"]
low_res  = ["2338x2338"]
high_res = ["5000x2338"]
wide_res = ["7016x3947"]

commands = [graph + ["STANDARD_ATLAS"] + date + high_res + ["latex/images/atlas.png"],
            graph + ["STANDARD_RING"] + date + low_res + ["latex/images/ring_1.png"],
            graph + ["STAGGERED_RING"] + date + low_res + ["latex/images/ring_2.png"],
            chart + ["ADDRESS_SPACE"] + date + low_res + ["latex/images/addr_space.png"],
            chart + ["YEARLY_BLOCKS"] + date + wide_res + ["latex/images/yr_blocks.png"]
            ]

child_processes = [Popen(command, shell=True) for command in commands]
counter         = len(commands)

for process in child_process:
    print("Still waiting for ",str(counter)," commands to finish")
    process.wait()
    counter -= 1

Popen(["pdflatex", "latex/main.tex"])
