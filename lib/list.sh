#!/bin/sh

ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

# package managers
ALL=0
APT=0
NPM=0
PACMAN=0
PIP=0
YARN=0
YAY=0

# options
QUIET=0
VERBOSE=0
COUNT=0
WITH_VERSION=0

# get arguments
PARSED_ARGUMENTS=$(getopt -n pacup-list -o qVcv --long quiet,verbose,count,with-version -- "$@")
eval set -- "$PARSED_ARGUMENTS"
while :; do
    case $1 in
        -q|--quiet)
            QUIET=1
            ;;
        -V|--verbose)
            VERBOSE=1
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
while :; do
    case $1 in
        all)
            ALL=1
            ;;
        apt)
            APT=1
            ;;
        npm)
            NPM=1
            ;;
        pacman)
            PACMAN=1
            ;;
        pip)
            PIP=1
            ;;
        yarn)
            YARN=1
            ;;
        yay)
            YAY=1
            ;;
        "")
            break
            ;;
        *)
            wrong_package_manager $1
            ;;
    esac
    shift
done

function get_packages {
    if $ROOTDIR/package-managers/$1/exists.sh; then
        if test $COUNT -eq 0; then
            [ $QUIET == 0 ] && print_success "EXPLICITLY INSTALLED PACKAGES FOR ${1^^}"
            IFS=$'\n' packages=($($ROOTDIR/package-managers/$1/get.sh))
            [ $WITH_VERSION = 0 ] && get_packageversion_human_format_name "${packages[@]}"
            [ $WITH_VERSION = 1 ] && get_packageversion_human_format "${packages[@]}"
        else
            count=$($ROOTDIR/package-managers/$1/get.sh | wc -l)
            [ $QUIET == 0 ] && print_success "NUMBER OF EXPLICITLY INSTALLED PACKAGES FOR ${1^^} IS $count"
        fi
    elif test $VERBOSE -eq 1; then
        [ $QUIET == 0 ] && print_warning "SKIPPING ${1^^} (NOT INSTALLED OR NOT IN PATH)"
    fi
}

if test $ALL -eq 1; then
    APT=1
    NPM=1
    PACMAN=1
    PIP=1
    YARN=1
    YAY=1
fi
if test $APT -eq 1; then
    get_packages apt
fi
if test $NPM -eq 1; then
    get_packages npm
fi
if test $PACMAN -eq 1; then
    get_packages pacman
fi
if test $PIP -eq 1; then
    get_packages pip
fi
if test $YARN -eq 1; then
    get_packages yarn
fi
if test $YAY -eq 1; then
    get_packages yay
fi
