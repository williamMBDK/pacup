#!/bin/sh

# imports
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/config.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

# option variables
CONFIG=0
PACLIST=0
WITH_VERSION=0
QUIET=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacup-status -o c:l:vq --long configuration:,package-list:,with-version,quiet -- "$@")
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
        -v|--with-version)
            WITH_VERSION=1
            shift
            ;;
        -q|--quiet)
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
! PACUP_SHOULD_FILTER_LISTS=1 PACUP_SHOULD_FILTER_CONFIGS=1 process_package_manager_arguments $@ && [ $QUIET != 1 ] && echo

function format_packageversion {
    packageversion="$1"
    if [ $WITH_VERSION = 0 ]; then
        get_packageversion_human_format_name "$packageversion"
    else
        get_packageversion_human_format "$packageversion"
    fi
}

function status_of_user_configuration {
    print_needed_info "STATUS OF USER CONFIGURATION"
    print_colored "GREEN" "USER LISTS DIRECTORY: $PACUP_LISTS_DIR"
    print_colored "GREEN" "USER CONFIGS DIRECTORY: $PACUP_CONFIGS_DIR"
}

function status_of_package_managers {
    print_needed_info "STATUS OF SUPPORTED PACKAGE MANAGERS"
    for package_manager in $(get_package_managers); do
        if ! does_package_manager_exist "$package_manager"; then 
            print_colored "CYAN" "$package_manager is not installed"
        elif ! does_package_manager_have_config "$package_manager" && ! does_package_manager_have_list "$package_manager"; then
            print_colored "CYAN" "$package_manager is installed"
        elif ! does_package_manager_have_config "$package_manager"; then
            print_colored "YELLOW" "$package_manager is installed and has a package list, but not a config"
        elif ! does_package_manager_have_list "$package_manager"; then
            print_colored "YELLOW" "$package_manager is installed and has a config, but not a package list"
        else
            print_colored "GREEN" "$package_manager is installed, has a package list and a config"
        fi
    done
}

function status_of_packages_for_package_manager {
    local CONFIG=$1
    local PACLIST=$2
    local PACMANAGER=$3
    print_needed_info "STATUS OF PACKAGES FOR ${PACMANAGER^^}"
    # check if matching packages are installed
    get_matches_and_handle_errors $CONFIG $PACLIST # set $matches
    (IFS=$'\n'
    for packageandversion in $matches; do
        if ! is_package_installed "$PACMANAGER" "$packageandversion"; then
            print_colored "YELLOW" "NOT INSTALLED OR NOT UP-TO-DATE: $(get_packageversion_human_format "$packageandversion")" # version is not optional here since version is part of the config
        fi
    done)

    explicits=$(get_packages_installed_for_package_manager $PACMANAGER)
    packages_in_paclist=$($ROOTDIR/run_module.sh "configuration.get_packages_in_list" "$PACLIST")

    # check if there are explicitly installed packages that are not a matched package or in list
    (IFS=$'\n'
    for packageandversion in $explicits; do
        if ! is_package_in_list "$packages_in_paclist" "$packageandversion"; then
            print_colored "CYAN" "INSTALLED BUT NOT IN PACKAGE LIST: $(format_packageversion "$packageandversion")"
        elif ! is_package_in_list "$matches" "$packageandversion"; then
            print_colored "BLUE" "INSTALLED, IN PACKAGE LIST BUT NOT IN CONFIG: $(format_packageversion "$packageandversion")"
        fi
    done)
}

function status_of_packages {
    # if no package managers are given then default to assume all of them are given
    if [ $(get_number_of_package_managers_provided) = "0" ]; then
        # for package_manager in $(get_package_managers); do
        #     declare -g "${package_manager^^}=1"
        # done
        # print_additional_info "no package managers given - defaulting to all"
        return 0
    fi
    print_needed_info "STATUS OF PACKAGES"
    # if only one package manager is given then we allow the -c and -l options
    if [ $(get_number_of_package_managers_provided) = "1" ]; then
        local package_manager
        for pm in $(get_package_managers); do
            local varname=${pm^^}
            if [ ${!varname} = 1 ]; then 
                package_manager=$pm
            fi
        done
        if [ $CONFIG = 0 ]; then
            CONFIG=$(get_config_for_package_manager $package_manager)
        fi
        if [ $PACLIST = 0 ]; then
            PACLIST=$(get_list_for_package_manager $package_manager)
        fi
        status_of_packages_for_package_manager "$CONFIG" "$PACLIST" "$package_manager"
    # otherwise we ignore -c and -l
    else
        [ $CONFIG != 0 ] && print_warning "Ignoring -c | --configuration since multiple package managers were given"
        [ $PACLIST != 0 ] && print_warning "Ignoring -l | --package-list since multiple package managers were given"
        for package_manager in $(get_package_managers); do
            local varname=${package_manager^^}
            if [ ${!varname} = 1 ]; then 
                status_of_packages_for_package_manager "$(get_config_for_package_manager $package_manager)" "$(get_list_for_package_manager $package_manager)" "$package_manager"
            fi
        done
    fi
}

status_of_user_configuration
echo
status_of_package_managers
echo
status_of_packages
