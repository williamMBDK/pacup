#!/bin/sh

# imports
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

# option variables
QUIET=0
CONFIG=0
PACLIST=0
TEST=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacup-install -o c:l:qt --long configuration:,package-list:,quiet,test -- "$@")
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

# get package managers
! PACUP_SHOULD_FILTER=1 process_package_manager_arguments $@ && [ $QUIET != 1 ] && (( $(get_number_of_package_managers_provided) > 0 )) && echo

function perform_installation {
    local PACMANAGER=$1
    local PACLIST=$2
    local CONFIG=$3

    [ $QUIET = 0 ] && print_needed_info "INSTALLATION OF PACKAGES FOR ${PACMANAGER^^}"

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
                print_additional_info "Package $(get_packageversion_human_format "$packageandversion") is installed"
            fi
        fi
    done)
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
    perform_installation "$package_manager" "$PACLIST" "$CONFIG"
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
            perform_installation "$package_manager" "$PACLIST" "$CONFIG"
            should_print_newline=1
        fi
    done
fi
