SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

package=$1
version=$2

cachedir="$HOME/.cache/pacup/snap"

mkdir -p $cachedir

if [[ $(find "$cachedir/get.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
    $SCRIPT_DIR/get.sh > $cachedir/get.out
fi

if [ "$#" -eq 1 ]; then
    if [[ $(find "$cachedir/update.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
        #  > $cachedir/update.out
        >&2 echo "missing implementation: implement update check for snap!"
    fi
    # cat $cachedir/update.out | grep $package > /dev/null && exit 1
    cat $cachedir/get.out | grep "^$package@" > /dev/null
else
    cat $cachedir/get.out | grep "^$package@$version$" > /dev/null
fi
