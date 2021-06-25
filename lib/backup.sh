#!/bin/bash

# imports
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

# option variables
PACLIST=0
QUIET=0
OUTPUT=0
WITH_VERSION=0
INTERACTIVE=0
YES=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacup-backup -o l:o:qviy -l package-list:,output:,quiet,with-version,interactive,yes -- "$@")
eval set -- "$PARSED_ARGUMENTS"
while :; do
    case $1 in
        -l | --package-list)
            PACLIST=$2
            shift 2
            ;;
        -o | --output)
            OUTPUT=$2
            shift 2
            ;;
        -q | --quiet)
            QUIET=1
            shift
            ;;
        -v | --with-version)
            WITH_VERSION=1
            shift
            ;;
        -i | --interactive)
            INTERACTIVE=1
            shift
            ;;
        -y | --yes)
            YES=1
            shift
            ;;
        --)
            shift
            break
            ;;
    esac
done

# get package managers
! PACUP_SHOULD_FILTER_LISTS=1 PACUP_SHOULD_FILTER_CONFIGS=0 process_package_manager_arguments $@ && [ $QUIET != 1 ] && (( $(get_number_of_package_managers_provided) > 0 )) && echo

function perform_backup {

    local PACMANAGER=$1
    local PACLIST=$2
    local OUTPUT=$3

    [ $QUIET = 0 ] && print_needed_info "BACKUP OF PACKAGES FROM ${PACMANAGER^^}"

    explicits=$(get_packages_installed_for_package_manager "$PACMANAGER")
    packages_in_paclist=$($ROOTDIR/run_module.sh "configuration.get_packages_in_list" "$PACLIST")

    # slow for loop!
    local packages_to_add=""
    for packageandversion in $explicits; do
        if ! is_package_in_list "$packages_in_paclist" "$packageandversion" ; then
            package=$(if [ $WITH_VERSION = 1 ]; then
                printf "$packageandversion"
            else
                get_packageversion_name "$packageandversion"
            fi)
            if [ $INTERACTIVE = 1 ]; then
                if lazy_confirm "Do you wish to add the following package to the package list: $package"; then
                    packages_to_add="$packages_to_add$package"$'\n'
                else
                    [ $QUIET = 0 ] && print_needed_info "Skipping $package"
                fi
            else
                packages_to_add="$packages_to_add$package"$'\n'
            fi
        fi
    done

    [ $(printf "$packages_to_add" | wc -l) = 0 ] && { [ $QUIET = 0 ] && print_warning "Nothing to backup for $PACMANAGER."; } && return 0

    if [[ $QUIET == 0 && $INTERACTIVE == 0 ]]; then
        print_needed_info "Packages installed but not in package list ($OUTPUT)"
        print_colored "GREEN" "$packages_to_add"
        { { [ $YES = 1 ] || lazy_confirm "Do you wish to add the above packages?"; } || { print_needed_info "Okay. skipping..." && return 0; }; }
    fi

    printf "$packages_to_add" | $ROOTDIR/run_module.sh "configuration.append_to_package_list" "$PACLIST" "$OUTPUT"
    [ $QUIET = 0 ] && print_success "Added packages to package-list ($OUTPUT)"
}

[ $(get_number_of_package_managers_provided) = "0" ] && exit 0

if [ $(get_number_of_package_managers_provided) = "1" ]; then
    package_manager=$(get_single_set_package_manager)
    if [ $PACLIST = 0 ]; then
        PACLIST=$(get_list_for_package_manager $package_manager)
    fi
    if [ $OUTPUT = 0 ]; then
        OUTPUT=$PACLIST
    fi
    perform_backup "$package_manager" "$PACLIST" "$OUTPUT"
else
    [ $PACLIST != 0 ] && print_warning "Ignoring -l | --package-list since multiple package managers were given"
    [ $OUTPUT != 0 ] && print_warning "Ignoring -o | --output since multiple package managers were given"
    should_print_newline=0
    for package_manager in $(get_package_managers); do
        varname=${package_manager^^}
        if [ ${!varname} = 1 ]; then 
            PACLIST="$(get_list_for_package_manager $package_manager)"
            OUTPUT=$PACLIST
            [ $should_print_newline = 1 ] && echo
            perform_backup "$package_manager" "$PACLIST" "$OUTPUT"
            should_print_newline=1
        fi
    done
fi

exit 0
