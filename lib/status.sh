#!/bin/sh

# imports
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/util.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

# option variables
CONFIG=0
PACLIST=0
PACMANAGER=0
WITH_VERSION=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacup-status -o c:l:p:v --long configuration:,package-list:,package-manager:with-version -- "$@")
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
        -v|--with-version)
            WITH_VERSION=1
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
exit_on_missing_option "$PACMANAGER" "-p | --package-manager"

# check that a valid package manager were given
exit_on_invalid_package_manager $PACMANAGER

# get matching packages
get_matches_and_handle_errors $CONFIG $PACLIST # set $matches

function format_packageversion {
    packageversion="$1"
    if [ $WITH_VERSION = 0 ]; then
        get_packageversion_human_format_name "$packageversion"
    else
        get_packageversion_human_format "$packageversion"
    fi
}

print_needed_info "STATUS OF PACKAGES"

# check if matching packages are installed
(IFS=$'\n'
for packageandversion in $matches; do
    if ! $SCRIPT_DIR/package-managers/$PACMANAGER/pac-installed.sh $packageandversion; then
        print_colored "YELLOW" "NOT INSTALLED OR UP-TO-DATE: $(get_packageversion_human_format "$packageandversion")" # version is not optional here since version is part of the config
    fi
done)

explicits=$($SCRIPT_DIR/package-managers/$PACMANAGER/get.sh)
packages_in_paclist=$($SCRIPT_DIR/run_module.sh "configuration.get_packages_in_list" "$PACLIST")

# check if there are explicitly installed packages that are not a matched package or in list
(IFS=$'\n'
for packageandversion in $explicits; do
    if ! is_package_in_list "$packages_in_paclist" "$packageandversion"; then
        print_colored "CYAN" "INSTALLED BUT NOT IN PACKAGE LIST: $(format_packageversion "$packageandversion")"
    elif ! is_package_in_list "$matches" "$packageandversion"; then
        print_colored "BLUE" "INSTALLED, IN PACKAGE LIST BUT NOT IN CONFIG: $(format_packageversion "$packageandversion")"
    fi
done)
