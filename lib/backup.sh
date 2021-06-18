#!/bin/sh

# imports
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

# option variables
PACMANAGER=0
PACLIST=0
QUIET=0
OUTPUT=0
WITH_VERSION=0
INTERACTIVE=0
YES=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacup-backup -o p:l:o:qviy -l package-manager:,package-list:,output:,quiet,with-version,interactive,yes -- "$@")
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

# missing options check
exit_on_missing_option "$PACMANAGER" "-p | --package-manager"
exit_on_missing_option "$PACLIST" "-l | --package-list"

# check that a valid package manager were given
exit_on_invalid_package_manager "$PACMANAGER"

explicits=$($ROOTDIR/package-managers/$PACMANAGER/get.sh)
packages_in_paclist=$($ROOTDIR/run_module.sh "configuration.get_packages_in_list" "$PACLIST")

# slow for loop!
packages_to_add=()
IFS=$'\n'
for packageandversion in $explicits; do
    if ! is_package_in_list "$packages_in_paclist" "$packageandversion" ; then
        package=$(if [ $WITH_VERSION = 1 ]; then
            printf "$packageandversion"
        else
            get_packageversion_name "$packageandversion"
        fi)
        if [ $INTERACTIVE = 1 ]; then
            if lazy_confirm "Do you wish to add the following package to the package list: $(get_packageversion_human_format $package)"; then
                packages_to_add+=($package)
            else
                [ $QUIET = 0 ] && print_needed_info "Skipping $(get_packageversion_human_format $package)"
            fi
        else
            packages_to_add+=($package)
        fi
    fi
done

[ ${#packages_to_add[@]} = 0 ] && { [ $QUIET = 0 ] && print_warning "Nothing to backup. Exiting..."; } && exit 0

if [[ $QUIET == 0 && $INTERACTIVE == 0 ]]; then
    print_needed_info "Packages installed but not in package list ($OUTPUT)"
    get_packageversion_human_format "${packages_to_add[@]}"
    { { [ $YES = 1 ] || lazy_confirm "Do you wish to add the above packages?"; } || { print_needed_info "Okay. skipping..." && exit 0; }; }
fi

printf "%s\n" "${packages_to_add[@]}" | $ROOTDIR/run_module.sh "configuration.append_to_package_list" "$PACLIST" "$OUTPUT"
[ $QUIET = 0 ] && print_success "Added packages to package-list ($OUTPUT)"

exit 0

