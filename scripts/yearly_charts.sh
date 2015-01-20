echo "Charting available IPv4 address space over time"
echo ""
echo ""

echo "Setting Up"
export PYTHONPATH=$HOME/honours-project
export GENERIC=$HOME/honours-project/parallel/generic
rm -rf temp

echo "Setting up directories"
mkdir temp
mkdir temp/parsed
mkdir temp/merged

echo "Locating available BGP files to parse"
python $GENERIC/list_year_end_files.py

echo "Parsing files"
parallel --no-notice -a temp/files_to_parse "python $GENERIC/parse_bgp_file.py"

echo "Merging parsed router data"
parallel --no-notice -a temp/files_to_merge "python $GENERIC/merge_parsed_dumps.py"

echo "Generating chart"
python $PYTHONPATH/parallel/yearly_charts.py

echo "Cleaning Up"
unset PYTHONPATH
unset GENERIC
rm -rf temp
