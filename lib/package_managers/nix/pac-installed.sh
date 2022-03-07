SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pac=$1
version=$2

if [ "$#" -eq 1 ]; then
    nix-env -q $pac # should check for updates but it is very slow
else
    nix-env -q $pac-$version
fi
