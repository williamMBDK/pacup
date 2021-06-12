#!/bin/sh

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

source $SCRIPT_DIR/color.sh
SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

function wrong_option {
    printf "${YELLOW}WARNING: Unknown option (ignored): %s\n${NOCOLOR}" "$1" >&2
}

function wrong_package_manager {
    printf "${YELLOW}WARNING: Unknown package manager (ignored): %s\n${NOCOLOR}" "$1" >&2
}

function err_option_value {
    printf "${RED}ERROR: Unknown option value for %s: %s\n${NOCOLOR}" "$1" "$2" >&2
}

function wrong_subcommand {
    printf "${RED}ERROR: Unknown subcommand: %s\n${NOCOLOR}" "$1" >&2
}

function config_path_not_exist {
    printf "${RED}ERROR: Configuration path does not exist: %s\n${NOCOLOR}" "$1" >&2
}

function showhelp {
    if (ls $SCRIPT_DIR/../man/pacback.1 >> /dev/null 2>&1) || (ls $SCRIPT_DIR/../man/pacback.txt >> /dev/null 2>&1); then
        $SCRIPT_DIR/../man/makeman.sh
    fi
    if command -v man > /dev/null; then
        man $SCRIPT_DIR/../man/pacback.1
    else
        cat $SCRIPT_DIR/../man/pacback.txt
    fi
}

function get_package_managers {
    ls -d $SCRIPT_DIR/package-managers/*/ | while read folder ; do
        echo -n "$(basename $folder) "
    done
}

function get_package_manager_pattern {
    get_package_managers | sed 's/ /|/g'
}
