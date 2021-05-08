#!/bin/sh

function wrong_option {
    printf 'WARNING: Unknown option (ignored): %s\n' "$1" >&2
}

function wrong_package_manager {
    printf 'WARNING: Unknown package manager (ignored): %s\n' "$1" >&2
}

function wrong_subcommand {
    printf 'ERROR: Unknown subcommand: %s\n' "$1" >&2
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
