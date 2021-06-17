#!/bin/sh

# imports
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

# option variables
QUIET=0
CONFIG=0
PACLIST=0
PACMANAGER=0
TEST=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacup-install -o c:l:p:qt --long configuration:,package-list:,package-manager:,quiet,test -- "$@")
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
        -t  | --test)
            TEST=1
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

# install matching packages
(IFS=$'\n'
for packageandversion in $matches; do
    if ! $ROOTDIR/package-managers/$PACMANAGER/pac-installed.sh $packageandversion; then
        if ! lazy_confirm "Do you wish to install $(get_packageversion_human_format "$packageandversion") using $PACMANAGER?"; then
            [ $QUIET = 0 ] && print_additional_info "Skipping $(get_packageversion_human_format "$packageandversion")"
            continue
        fi
        [ $QUIET = 0 ] && print_needed_info "Beginning installation of $(get_packageversion_human_format "$packageandversion") using $PACMANAGER"
        [ $QUIET = 0 ] && printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' = # fill width of display with '='
        exit_code=0
        if [ $TEST = 0 ]; then
            $ROOTDIR/package-managers/$PACMANAGER/install.sh $(get_packageversion_name $packageandversion) $(get_packageversion_version $packageandversion) # why cant i just give $packageandversion as argument?
            exit_code=$?
        fi
        [ $QUIET = 0 ] && printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' = # fill width of display with '='
        [ $QUIET = 0 ] && [ $exit_code = 0 ] && print_success "Installed $(get_packageversion_human_format "$packageandversion") using $PACMANAGER"
        [ $exit_code != 0 ] && print_error "Something went wrong during installation of $(get_packageversion_human_format "$packageandversion") using $PACMANAGER"
    else
        if test $QUIET -eq 0; then
            print_additional_info "Skipping $(get_packageversion_human_format "$packageandversion")"
        fi
    fi
done)
