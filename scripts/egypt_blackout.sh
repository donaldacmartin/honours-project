echo "Creating GIF of the Egypt Internet Blackout"

echo "Setting Up"
export ROOT_DIR=$HOME/honours-project
export WORKING_DIR=$ROOT_DIR/parallel/internet_blackouts/egypt_2011
export PYTHONPATH=:$ROOT_DIR
rm -rf $ROOT_DIR/temp
mkdir $ROOT_DIR/temp

echo "Generating a list of files to parse"
python $WORKING_DIR/setup_files.py

echo "Parsing files"
mkdir $ROOT_DIR/temp/parsed
parallel --no-notice -a temp/parsing_index "python $WORKING_DIR/parse_file.py"

echo "Merging parsed outputs"
mkdir temp/merged
parallel --no-notice --xapply -a temp/merging_index "python $WORKING_DIR/merge_dumps.py"

echo "Generating graph frames"
mkdir graphs
parallel --no-notice --xapply -a temp/diff_index_1 -a temp/diff_index_2 "python $WORKING_DIR/draw_graph.py"