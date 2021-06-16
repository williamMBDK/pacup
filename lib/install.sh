#!/bin/sh

# imports
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/util.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))
source $SCRIPT_DIR/utility/color.sh
SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

# option variables
QUIET=0
CONFIG=0
PACLIST=0
PACMANAGER=0
TEST=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacback-install -o c:l:p:qt --long configuration:,package-list:,package-manager:,quiet,test -- "$@")
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
if test $CONFIG = 0; then
    err_missing_option "-c | --configuration"
    exit 1
fi
if test $PACLIST = 0; then
    err_missing_option "-l | --package-list"
    exit 1
fi
if [ $PACMANAGER = 0 ]; then
    err_missing_option "-p | -package-manager"
    exit 1
fi

# check that a valid package manager were given
valid_package_manager=0
for package_manager in $(get_package_managers); do
    if [ "$package_manager" = $PACMANAGER ]; then
        valid_package_manager=1
    fi
done
if test $valid_package_manager -eq 0; then
    err_option_value "-p | --package-manager" "$PACMANAGER"
    exit 1
fi

# get matching packages
matches=$($SCRIPT_DIR/config-match.py $CONFIG $PACLIST)
exit_code=$?

# handle error during matching
if test $exit_code != 0; then
    print_error "$matches"
    exit $exit_code
fi

# install matching packages
printf "$matches" | while read -r packageandversion ; do
    if ! $SCRIPT_DIR/package-managers/$PACMANAGER/pac-installed.sh $packageandversion; then
        if test $QUIET -eq 0; then
            print_needed_info "Beginning installation of $packageandversion using $PACMANAGER"
            printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' = # fill width of display with '='
            if [ $TEST = 0 ]; then
                $SCRIPT_DIR/package-managers/$PACMANAGER/install.sh $packageandversion
            fi
            printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' = # fill width of display with '='
            print_success "Installed $packageandversion using $PACMANAGER"
        fi
    else
        if test $QUIET -eq 0; then
            print_additional_info "Skipping $packageandversion"
        fi
    fi
done
