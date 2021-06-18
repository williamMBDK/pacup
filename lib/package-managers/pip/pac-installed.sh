SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

package=$1
version=$2

cachedir="$HOME/.cache/pacup/pip"

mkdir -p $cachedir

if [[ $(find "$cachedir/pipget.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
    $SCRIPT_DIR/get.sh > $cachedir/pipget.out
fi

if [ "$#" -eq 1 ]; then
    if [[ $(find "$cachedir/pipupdate.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
        pip list --user -o --not-required 2> /dev/null > $cachedir/pipupdate.out
    fi
    cat $cachedir/pipupdate.out | grep "^$package " > /dev/null && exit 1
    cat $cachedir/pipget.out | grep "^$package " > /dev/null
else
    cat $cachedir/pipget.out | grep "^$package $version$" > /dev/null
fi
