SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pac=$1
version=$2

if [ "$#" -eq 1 ]; then
    cachedir="$HOME/.cache/pacback/yay"
    mkdir -p $cachedir
    if [[ $(find "$cachedir/yayqu.out" -newermt '-3 seconds') == "" ]]; then
        touch $cachedir/yayqu.out
        yay -Qu > $cachedir/yayqu.out
    fi
    cat $cachedir/yayqu.out | grep "^$pac " > /dev/null && exit 1
    exit 0
else
    $SCRIPT_DIR/get.sh | grep "^$pac $version$" > /dev/null
fi

