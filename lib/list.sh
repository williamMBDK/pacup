#!/bin/sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel

source $SCRIPT_DIR/util.sh
source $SCRIPT_DIR/color.sh

ALL=0
APT=0
NPM=0
PACMAN=0
PIP=0
YARN=0
YAY=0

QUIET=0
VERBOSE=0

# https://gist.github.com/deshion/10d3cb5f88a21671e17a
while :; do
    case $1 in
        -h|-\?|--help)
            showhelp
            exit
            ;;
        -q|--quiet)
            QUIET=1
            ;;
        -v|--verbose)
            VERBOSE=1
            ;;
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
        -?*)
            wrong_option $1
            ;;
        *)
            wrong_package_manager $1
            ;;
    esac
    shift
done

function print {
    if test $QUIET -eq 0; then
        echo -e $1
    fi
}

function get_packages {
    if $SCRIPT_DIR/$1/exists.sh; then
        print "${GREEN}EXPLICITLY INSTALLED PACKAGES FOR ${1^^}${NOCOLOR}"
        $SCRIPT_DIR/$1/get.sh
    elif test $VERBOSE -eq 1; then
        print "${YELLOW}SKIPPING ${1^^} (NOT INSTALLED OR NOT IN PATH)${NOCOLOR}"
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
