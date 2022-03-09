SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pac=$1
version=$2

if [ "$#" -eq 2 ]; then
    echo "version not supported by nix"
    exit 2
fi

cachedir="$HOME/.cache/pacup/nix"

mkdir -p $cachedir

if [[ $(find "$cachedir/installed.txt" -newermt '-5 seconds' 2>/dev/null) == "" ]]; then
    $SCRIPT_DIR/get.sh > $cachedir/installed.txt
fi

cat $cachedir/installed.txt | grep "^$pac@unsupported" > /dev/null
