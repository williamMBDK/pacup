#!/bin/sh

# imports
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/util.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/color.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

# option variables
QUIET=0
CONFIG=0
PACLIST=0
PACMANAGER=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacback-install -o c:l:p:q --long configuration:,package-list:,package-manager:,quiet -- "$@")
eval set -- "$PARSED_ARGUMENTS"
while :; do
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

# check that a valid package manager were given
if [ $PACMANAGER = 0 ]; then
    err_missing_option "-p | -package-manager"
    exit 1
fi
valid_package_manager=0
for package_manager in $(get_package_managers); do
    if [ "$package_manager" = $PACMANAGER ]; then
        valid_package_manager=1
    fi
done
if test $valid_package_manager -eq 0; then
    err_option_value "-p | --package-manager" "$PACMANAGER"
    exit 1
fi

# install matching packages
$SCRIPT_DIR/config-match.py -q -c $CONFIG -l $PACLIST | while read -r packageandversion ; do
    if ! $SCRIPT_DIR/package-managers/$PACMANAGER/pac-installed.sh $packageandversion; then
        if test $QUIET -eq 0; then
            echo Installing package with $PACMANAGER: $packageandversion
        fi
    else
        if test $QUIET -eq 0; then
            print_info "Skipping $packageandversion"
        fi
    fi
done
