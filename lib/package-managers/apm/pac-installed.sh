SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

package=$1
version=$2

cachedir="$HOME/.cache/pacup/apm"

mkdir -p $cachedir

if [[ $(find "$cachedir/get.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
    $SCRIPT_DIR/get.sh > $cachedir/get.out
fi

if [ "$#" -eq 1 ]; then
    if [[ $(find "$cachedir/update.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
        apm --no-color update -l | awk '{print $2}' | tail -n +2 2> /dev/null | tail -n +2 > $cachedir/update.out
    fi
    cat $cachedir/update.out | grep $package > /dev/null && exit 1
    cat $cachedir/get.out | grep "^$package@" > /dev/null
else
    cat $cachedir/get.out | grep "^$package@$version$" > /dev/null
fi
