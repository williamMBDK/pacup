#!/bin/sh

# imports
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/util.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

# option variables
PACMANAGER=0
PACLIST=0
QUIET=0
OUTPUT=0
WITH_VERSION=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacback-backup -o p:l:o:qv -l package-manager:,package-list:,output:,quiet,with-version -- "$@")
eval set -- "$PARSED_ARGUMENTS"
while :; do
    case $1 in
        -p | --package-manager)
            PACMANAGER=$2
            shift 2
            ;;
        -l | --package-list)
            PACLIST=$2
            [ $OUTPUT = 0 ] && OUTPUT=$PACLIST
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
        --)
            shift
            break
            ;;
    esac
done

# missing options check
exit_on_missing_option "$PACMANAGER" "-p | --package-manager"
exit_on_missing_option "$PACLIST" "-l | --package-list"

# check that a valid package manager were given
exit_on_invalid_package_manager "$PACMANAGER"

explicits=$($SCRIPT_DIR/package-managers/$PACMANAGER/get.sh)
packages_in_paclist=$($SCRIPT_DIR/run_module.sh "configuration.get_packages_in_list" "$PACLIST")

packages_to_add=$(IFS=$'\n'
for packageandversion in $explicits; do
    if ! is_package_in_list "$packages_in_paclist" "$packageandversion" ; then
        if [ $WITH_VERSION = 1 ]; then
            printf "$packageandversion\n"
        else
            get_packageversion_name "$packageandversion"
        fi
    fi
done)

[ $(printf "$packages_to_add" | wc -l) = 0 ] && { [ $QUIET = 0 ] && print_warning "Nothing to backup. Exiting..."; } && exit 0
[ $QUIET = 0 ] && print_needed_info "Packages installed but not in package list ($OUTPUT)"
[ $QUIET = 0 ] && printf "$packages_to_add\n"
[ $QUIET = 0 ] && { lazy_confirm "Do you wish to add the above packages?" || { print_needed_info "Okay. skipping..." && exit 0; }; }

printf "$packages_to_add" | $SCRIPT_DIR/run_module.sh "configuration.append_to_package_list" "$PACLIST" "$OUTPUT"
[ $QUIET = 0 ] && print_success "Added packages to package-list ($OUTPUT)"

exit 0

