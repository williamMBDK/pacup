#!/bin/sh

ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

# options
QUIET=0
COUNT=0
WITH_VERSION=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacup-list -o qcv --long quiet,count,with-version -- "$@")
eval set -- "$PARSED_ARGUMENTS"
while :; do
    case $1 in
        -q|--quiet)
            QUIET=1
            ;;
        -c|--count)
            COUNT=1
            ;;
        -v|--with-version)
            WITH_VERSION=1
            ;;
        --)
            shift
            break
            ;;
    esac
    shift
done

# get package managers
process_package_manager_arguments $@

function get_packages {
    if test $COUNT -eq 0; then
        [ $QUIET == 0 ] && print_success "EXPLICITLY INSTALLED PACKAGES FOR ${1^^}"
        packages=$(get_packages_installed_for_package_manager "$1")
        [ $WITH_VERSION = 0 ] && get_packageversion_list_names "$packages"
        [ $WITH_VERSION = 1 ] && printf "$packages\n"
    else
        count=$(get_packages_installed_for_package_manager "$1" | wc -l)
        [ $QUIET == 0 ] && print_success "NUMBER OF EXPLICITLY INSTALLED PACKAGES FOR ${1^^} IS $count"
    fi
}

for package_manager in $(get_package_managers); do
    varname=${package_manager^^}
    if [ ${!varname} = 1 ]; then
        get_packages "$package_manager"
    fi
done

