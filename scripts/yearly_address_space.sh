echo "Charting available IPv4 address space over time"
echo ""
echo ""

echo "Setting Up"
export PARALLEL=$HOME/honours-project/parallel
export GENERIC=$PARALLEL/generic

export PYTHONPATH=:$HOME/honours-project
rm -rf temp

echo "Setting up directories"
mkdir temp
mkdir temp/parsed
MKDIR temp/merged

echo "Locating available BGP files to parse"
python $GENERIC/list_year_end_files.py

echo "Parsing files"
parallel --no-notice -a temp/files_to_parse "python $GENERIC/parse_bgp_file.py"

echo "Merging parsed router data"
parallel --no-notice -a temp/files_to_merge "python $GENERIC/merge_parsed_dumps.py"

echo "Generating chart"
python $PARALLEL/draw_yearly_address_space.py

echo "Cleaning Up"
unset PYTHONPATH
