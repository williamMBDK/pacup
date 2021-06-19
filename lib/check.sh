#!/bin/sh

# imports
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

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

# get package managers
! PACUP_SHOULD_FILTER_LISTS=1 PACUP_SHOULD_FILTER_CONFIGS=1 process_package_manager_arguments $@ && [ $QUIET != 1 ] && (( $(get_number_of_package_managers_provided) > 0 )) && echo

function perform_check {
    local PACMANAGER=$1
    local PACLIST=$2
    local CONFIG=$3
    # get matches
    [ $QUIET = 0 ] && print_success "MATCHED PACKAGES FOR ${PACMANAGER^^}"
    get_matches_and_handle_errors $CONFIG $PACLIST # will exit on error
    local IFS=$'\n'
    match_list=($matches)
    get_packageversion_human_format "${match_list[@]}"
}

[ $(get_number_of_package_managers_provided) = "0" ] && exit 0

if [ $(get_number_of_package_managers_provided) = "1" ]; then
    package_manager=$(get_single_set_package_manager)
    if [ $PACLIST = 0 ]; then
        PACLIST=$(get_list_for_package_manager $package_manager)
    fi
    if [ $CONFIG = 0 ]; then
        CONFIG=$(get_config_for_package_manager $package_manager)
    fi
    perform_check "$package_manager" "$PACLIST" "$CONFIG"
else
    should_print_newline=0
    [ $PACLIST != 0 ] && [ $QUIET = 0 ] && print_warning "Ignoring -l | --package-list since multiple package managers were given" && should_print_newline=1
    [ $CONFIG != 0 ] && [ $QUIET = 0 ] && print_warning "Ignoring -c | --config since multiple package managers were given" && should_print_newline=1
    for package_manager in $(get_package_managers); do
        varname=${package_manager^^}
        if [ ${!varname} = 1 ]; then 
            PACLIST="$(get_list_for_package_manager $package_manager)"
            CONFIG="$(get_config_for_package_manager $package_manager)"
            [ $should_print_newline = 1 ] && echo
            perform_check "$package_manager" "$PACLIST" "$CONFIG"
            should_print_newline=1
        fi
    done
fi
