ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
module=$1
shift
cd $ROOTDIR
python3 -m $module $@ # todo: does this preserve the given arguments in quotes "arg1 .." "arg2 .."
