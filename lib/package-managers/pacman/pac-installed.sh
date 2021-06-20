SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pac=$1
version=$2
cachedir="$HOME/.cache/pacup/pacman"

mkdir -p $cachedir

if [[ $(find "$cachedir/pacmanqe.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
    touch $cachedir/pacmanqe.out
    $SCRIPT_DIR/get.sh > $cachedir/pacmanqe.out
fi

if [ "$#" -eq 1 ]; then
    if [[ $(find "$cachedir/pacmanqu.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
        touch $cachedir/pacmanqu.out
        pacman -Qu > $cachedir/pacmanqu.out
    fi
    cat $cachedir/pacmanqu.out | grep "^$pac " > /dev/null && exit 1
    cat $cachedir/pacmanqe.out | grep "^$pac@" > /dev/null
else
    cat $cachedir/pacmanqe.out | grep "^$pac@$version$" > /dev/null
fi
