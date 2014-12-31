#!/bin/sh

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

python parallel/file_lister.py
echo "Parsing BGP files"
parallel --no-notice -a temp/bgp_files "python parallel/bgp_parser.py"
echo "Generating graphs from BGP data"
parallel --no-notice --xapply -a temp/graph_args_1 -a temp/graph_args_2 "python parallel/generate_graph.py"
echo "Creating GIF"
python parallel/create_gif.py big.gif
echo "Cleaning up"
rm -rf temp
