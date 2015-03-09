from sys import argv

# Atlas Map -> (7016, 3947)
# Rest      -> (2338, 2338)

Popen("python scripts/plot_graph.py STANDARD_ATLAS 01/06/2014 7016x3947 scripts/latex/images/atlas.png", shell=True)
Popen("python scripts/plot_graph.py STANDARD_RING 01/06/2014 2338x2338 scripts/latex/images/ring_1.png", shell=True)
Popen("python scripts/plot_graph.py STAGGERED_RING 01/06/2014 2338x2338 scripts/latex/images/ring_2.png", shell=True)

Popen("python scripts/plot_chart.py ADDRESS_SPACE 2338x2338 scripts/latex/images/addr_space.png", shell=True)
Popen("python scripts/plot_chart.py YEARLY_BLOCKS 5000x2338 scripts/latex/images/yr_blocks.png", shell=True)
