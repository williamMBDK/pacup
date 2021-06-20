SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pac=$1
version=$2
cachedir="$HOME/.cache/pacup/yay"

mkdir -p $cachedir

if [[ $(find "$cachedir/yayqe.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
    touch $cachedir/yayqe.out
    $SCRIPT_DIR/get.sh > $cachedir/yayqe.out
fi

if [ "$#" -eq 1 ]; then
    if [[ $(find "$cachedir/yayqu.out" -newermt '-6 seconds' 2>/dev/null) == "" ]]; then
        touch $cachedir/yayqu.out
        yay -Qu > $cachedir/yayqu.out
    fi
    cat $cachedir/yayqu.out | grep "^$pac " > /dev/null && exit 1
    cat $cachedir/yayqe.out | grep "^$pac@" > /dev/null
else
    cat $cachedir/yayqe.out | grep "^$pac@$version$" > /dev/null
fi
