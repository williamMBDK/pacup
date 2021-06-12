SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

manager=$1
pac=$2
version=""

if [ "$#" -eq 2 ]; then
    version=$(yay -S --print-format %v $pac)
else
    version=$3
fi

$SCRIPT_DIR/$manager/get.sh | grep "^$pac@$version$" > /dev/null
