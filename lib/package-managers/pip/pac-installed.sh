SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

package=$1
version=$2

cachedir="$HOME/.cache/pacup/pip"

if [ "$#" -eq 1 ]; then
    # can be optimized with cache files
    pip list --user -o --not-required 2> /dev/null | grep "^$package " > /dev/null && exit 1
    $SCRIPT_DIR/get.sh | grep "^$package " > /dev/null
else
    $SCRIPT_DIR/get.sh | grep "^$package $version$" > /dev/null
fi
