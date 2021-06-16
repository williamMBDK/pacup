#!/bin/sh

# imports
SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
source $SCRIPT_DIR/color.sh
SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

# fundamental printf's
function print_warning {
    printf "${YELLOW}PACBACK WARNING: %s\n${NOCOLOR}" "$1" >&2
}
function print_error {
    printf "${RED}PACBACK ERROR: %s\n${NOCOLOR}" "$1" >&2
}
function print_additional_info {
    printf "${CYAN}PACBACK INFO: %s\n${NOCOLOR}" "$1"
}
function print_success {
    printf "${GREEN}PACBACK: %s\n${NOCOLOR}" "$1"
}
function print_needed_info {
    printf "PACBACK: %s\n" "$1"
}

# specialized versions of above
function wrong_option {
    print_warning "Unknown option (ignored): $1"
}
function wrong_package_manager {
    print_warning "Unknown package manager (ignored): $1"
}
function err_option_value {
    print_error "Invalid option value for $1: $2"
}
function err_missing_option {
    print_error "option $1 is required"
}
function wrong_subcommand {
    print_error "Invalid subcommand: $1"
}
function config_path_not_exist {
    print_error "Configuration path does not exist: $1"
}

# help
function show_help {
    if (ls $SCRIPT_DIR/../man/pacback.1 >> /dev/null 2>&1) || (ls $SCRIPT_DIR/../man/pacback.txt >> /dev/null 2>&1); then
        $SCRIPT_DIR/../man/makeman.sh
    fi
    if command -v man > /dev/null; then
        man $SCRIPT_DIR/../man/pacback.1
    else
        cat $SCRIPT_DIR/../man/pacback.txt
    fi
}

# package managers
function get_package_managers {
    ls -d $SCRIPT_DIR/package-managers/*/ | while read folder ; do
        echo -n "$(basename $folder) "
    done
}
function get_package_manager_pattern {
    get_package_managers | sed 's/ /|/g'
}
