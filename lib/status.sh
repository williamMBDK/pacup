#!/bin/sh

# imports
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/util.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

# option variables
CONFIG=0
PACLIST=0
PACMANAGER=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacback-install -o c:l:p: --long configuration:,package-list:,package-manager: -- "$@")
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
        --)
            shift
            break
            ;;
    esac
done

# missing options check
if test $CONFIG = 0; then
    err_missing_option "-c | --configuration"
    exit 1
fi
if test $PACLIST = 0; then
    err_missing_option "-l | --package-list"
    exit 1
fi
if [ $PACMANAGER = 0 ]; then
    err_missing_option "-p | -package-manager"
    exit 1
fi

# check that a valid package manager were given
if ! is_valid_package_manager $PACMANAGER; then
    err_option_value "-p | --package-manager" "$PACMANAGER"
    exit 1
fi

# get matching packages
get_matches_and_handle_errors $CONFIG $PACLIST # set $matches

# check if matching packages are installed
(IFS=$'\n'
for packageandversion in $matches; do
    if ! $SCRIPT_DIR/package-managers/$PACMANAGER/pac-installed.sh $packageandversion; then
        print_colored "YELLOW" "NOT INSTALLED OR UP-TO-DATE: $packageandversion"
    fi
done)

# check if there are explicitely installed packages that are not a matched package
explicits=$($SCRIPT_DIR/package-managers/$PACMANAGER/get.sh)
(IFS=$'\n'
for packageandversion in $explicits; do
    if ! $SCRIPT_DIR/package-managers/is_pac_in_config.sh "$matches" "$packageandversion"; then
        print_colored "CYAN" "INSTALLED BUT NOT IN CONFIG: $packageandversion"
    fi
done)
