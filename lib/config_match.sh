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
PARSED_ARGUMENTS=$(getopt -n pacup-config-match -o c:l:q -l configuration:,package-list:,quiet -- "$@")
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
exit_on_missing_option "$CONFIG" "-c | --configuration"
exit_on_missing_option "$PACLIST" "-l | --package-list"

# get matches
get_matches_and_handle_errors $CONFIG $PACLIST # will exit on error
if test $QUIET = 0; then
    print_success "MATCHED PACKAGES"
fi
IFS=$'\n'
match_list=($matches)
get_packageversion_human_format "${match_list[@]}"
