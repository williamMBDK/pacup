#!/bin/sh

# imports
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/util.sh
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

# get matching packages
matches=$($SCRIPT_DIR/config-match.py $CONFIG $PACLIST)
exit_code=$?

# handle error during matching
if test $exit_code != 0; then
    print_error "$matches"
    exit $exit_code
fi

# check if matching packages are installed
(IFS=$'\n'
for packageandversion in $matches; do
    if ! $SCRIPT_DIR/package-managers/$PACMANAGER/pac-installed.sh $packageandversion; then
        print_colored "YELLOW" "NOT INSTALLED: $packageandversion"
    fi
done)

# check if there are explicitely installed packages that are not a matched package
explicits=$($SCRIPT_DIR/package-managers/$PACMANAGER/get.sh)
(IFS=$'\n'
for packageandversion in $explicits; do
    package=$(echo $packageandversion  | head -n1 | cut -d " " -f1)
    if ! printf "$matches" | grep "^$packageandversion$" > /dev/null && ! printf "$matches" | grep "^$package$" > /dev/null; then
        print_colored "CYAN" "INSTALLED BUT NOT IN CONFIG: $packageandversion"
    fi
done)
