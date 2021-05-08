#!/bin/sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel

source $SCRIPT_DIR/color.sh

function wrong_option {
    printf "${YELLOW}WARNING: Unknown option (ignored): %s\n${NOCOLOR}" "$1" >&2
}

function wrong_package_manager {
    printf "${YELLOW}WARNING: Unknown package manager (ignored): %s\n${NOCOLOR}" "$1" >&2
}

function wrong_subcommand {
    printf "${RED}ERROR: Unknown subcommand: %s\n${NOCOLOR}" "$1" >&2
}

function showhelp {
    if (ls $SCRIPT_DIR/../man/pacback.1 >> /dev/null 2>&1) || (ls $SCRIPT_DIR/../man/pacback.txt >> /dev/null 2>&1); then
        echo heythere
        $SCRIPT_DIR/../man/makeman.sh
    fi
    if command -v man > /dev/null; then
        man $SCRIPT_DIR/../man/pacback.1
    else
        cat $SCRIPT_DIR/../man/pacback.txt
    fi
}
