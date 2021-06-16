#!/bin/sh

# imports
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/util.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

# option variables
QUIET=0
CONFIG=0
PACLIST=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacback-install -o c:l:q -l configuration:,package-list:,quiet -- "$@")
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

# get matches
matches=$($SCRIPT_DIR/config-match.py $CONFIG $PACLIST)
exit_code=$?
# test for any errors
if test $exit_code = 0; then
    if test $QUIET = 0; then
        print_success "MATCHED PACKAGES"
    fi
    printf "$matches"
else
    print_error "$matches"
    exit $exit_code
fi
