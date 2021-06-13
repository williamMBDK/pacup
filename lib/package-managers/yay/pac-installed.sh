SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pac=$1
version=$2

if [ "$#" -eq 1 ]; then
    yay -Qu $pac | grep $pac && exit 1
    exit 0
else
    $SCRIPT_DIR/get.sh | grep "^$pac $version$" > /dev/null
fi

