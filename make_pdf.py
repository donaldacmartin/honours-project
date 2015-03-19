from sys import argv
from subprocess import Popen

# Atlas Map -> (7016, 3947)
# Rest      -> (2338, 2338)

graph    = ["python", "plot_graph.py"]
chart    = ["python", "plot_chart.py"]
dtime    = ["python", "plot_downtime.py"]
date     = ["01/06/2014"]
low_res  = ["2338x2338"]
high_res = ["5000x2338"]
wide_res = ["7016x3947"]

commands = [graph + ["STANDARD_ATLAS"] + date + high_res + ["latex/images/atlas.png"],
            graph + ["STANDARD_RING"] + date + low_res + ["latex/images/ring.png"],
            graph + ["STAGGERED_RING"] + date + low_res + ["latex/images/staggered_ring.png"],
            chart + ["ADDRESS_SPACE"] + date + ["prefix=latex/images"] + low_res,
            chart + ["YEARLY_BLOCKS"] + date + ["prefix=latex/images"] + wide_res,
            dtime + ["EGY"] + ["27/01/2011", "29/01/2011"] + low_res + ["latex/images/egypt.png"] + ["1"],
            dtime + ["LIB"] + ["18/02/2011", "22/02/2011"] + low_res + ["latex/images/libya.png"] + ["1"],
            dtime + ["IND"] + ["30/01/2008", "31/01/2008"] + low_res + ["latex/images/india.png"] + ["1"]
            ]

counter = 1

for command in commands:
    print("Executing",str(counter),"of",str(len(commands)))
    process = Popen(command)
    process.wait()
    counter += 1

latex_generator = Popen(["pdflatex", "latex/main.tex"])
latex_generator.wait()
