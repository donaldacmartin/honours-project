echo "Setting Up"
export ROOTDIR=$HOME/honours-project
export PYTHONPATH=:$ROOTDIR
rm -rf $ROOTDIR/temp
mkdir $ROOTDIR/temp

echo "Generating a list of files to parse"
python $ROOTDIR/parallel/file_lister.py

echo "Parsing files"
parallel --no-notice -a temp/dumps "python $ROOTDIR/parallel/parser.py"
rm -rf $ROOTDIR/dumps

echo "Merging router dumps"
parallel --no-notice -a temp/years "python $ROOTDIR/parallel/merge_dumps.py"
rm -rf _nas05*

echo "Creating yearly diff frames"

rm -rf $ROOTDIR/years

echo "Cleaning up"
unset PYTHONPATH
unset ROOTDIR
