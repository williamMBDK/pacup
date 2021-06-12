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

PARSED_ARGUMENTS=$(getopt -n pacback-install -o c:l:p:q --long configuration,package-list,package-manager:,quiet: -- "$@")

eval set -- "$PARSED_ARGUMENTS"

while :
do
    case $1 in
        -c | --configuration)
            CONFIG=$2
            shift 2
            ;;
        -l | --package-list)
            PACLIST=$2
            shift 2
            ;;
        -p | --package-manager)
            PACMANAGER=$2
            shift 2
            ;;
        -q | --quiet)
            QUIET=1
            shift
            ;;
        --)
            shift
            break
            ;;
    esac
done

echo Config: $CONFIG
echo Paclist: $PACLIST
echo Manager: $PACMANAGER
echo Quiet: $QUIET

$SCRIPT_DIR/config-match.py -q -c $CONFIG -p $PACLIST | while read -r package ; do
    if test $QUIET -eq 0; then
        echo Installing package with $PACMANAGER: $package
    fi
done
