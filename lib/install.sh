#!/bin/sh

SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/util.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/color.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

QUIET=0
CONFIG=0
PACLIST=0
PACMANAGER=0

while getopts "c:l:p:q" opt; do
    case $opt in
        c)
            CONFIG=$OPTARG
            ;;
        l)
            PACLIST=$OPTARG
            ;;
        p)
            PACMANAGER=$OPTARG
            ;;
        q)
            QUIET=1
    esac
done

$SCRIPT_DIR/config-match.py -q -c $CONFIG -p $PACLIST | while read -r package ; do
    if test $QUIET -eq 0; then
        echo Installing package with $PACMANAGER: $package
    fi
done
