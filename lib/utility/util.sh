#!/bin/sh

# imports
SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
source $SCRIPT_DIR/color.sh
SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

# fundamental printf's
function print_warning {
    printf "${YELLOW}PACUP WARNING: %s\n${NOCOLOR}" "$1" >&2
}
function print_error {
    printf "${RED}PACUP ERROR: %s\n${NOCOLOR}" "$1" >&2
}
function print_additional_info {
    printf "${CYAN}PACUP INFO: %s\n${NOCOLOR}" "$1"
}
function print_success {
    printf "${GREEN}PACUP: %s\n${NOCOLOR}" "$1"
}
function print_needed_info {
    printf "PACUP: %s\n" "$1"
}
function print_needed_info_no_newline {
    printf "PACUP: %s" "$1"
}
function print_colored {
    printf "${!1}%s\n${NOCOLOR}" "$2"
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

# user input
function lazy_confirm {
    print_needed_info_no_newline "$1 [Y\n]: "
    read ans
    if [ "$ans" = "n" ]; then
        return 1
    else
        return 0
    fi
}

# help
function show_help {
    if ! ls $SCRIPT_DIR/../man/pacup.1 >> /dev/null 2>&1 || ! ls $SCRIPT_DIR/../man/pacup.txt >> /dev/null 2>&1; then
        $SCRIPT_DIR/../man/makeman.sh
    fi
    if command -v man > /dev/null; then
        man $SCRIPT_DIR/../man/pacup.1
    else
        cat $SCRIPT_DIR/../man/pacup.txt
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
function is_valid_package_manager {
    valid_package_manager=1
    for package_manager in $(get_package_managers); do
        if [ "$package_manager" = $PACMANAGER ]; then
            valid_package_manager=0
        fi
    done
    return $valid_package_manager
}

# other
function get_matches_and_handle_errors {
    CONFIG=$1
    PACLIST=$2
    matches=$($SCRIPT_DIR/run_module.sh "configuration.config_match" "$CONFIG" "$PACLIST")
    exit_code=$?

    # handle error during matching
    if test $exit_code != 0; then
        print_error "$matches"
        exit $exit_code
    fi
}
function exit_on_invalid_package_manager {
    PACMANAGER=$1
    if ! is_valid_package_manager $PACMANAGER; then
        err_option_value "-p | --package-manager" "$PACMANAGER"
        exit 1
    fi
}
function exit_on_missing_option {
    OPTION_VALUE=$1
    OPTION_DESC=$2
    if [ $OPTION_VALUE = 0 ]; then
        err_missing_option "$OPTION_DESC"
        exit 1
    fi
}

# packages
function get_packageversion_name {
    packageandversion=$1
    printf $packageandversion  | head -n1 | cut -d " " -f1
}
function get_packageversion_version {
    packageandversion=$1
    printf $packageandversion | awk '{print $2}'
}
function is_package_in_list {
    list=$1
    packageandversion=$2

    package=$(get_packageversion_name "$packageandversion")

    if ! printf "$list" | grep "^$packageandversion$" > /dev/null && ! printf "$list" | grep "^$package$" > /dev/null; then
        return 1
    fi
    return 0
}
function get_packageversion_human_format_name {
    while :; do
        [ "$1" = "" ] && break
        name=$(get_packageversion_name $1)
        printf "$name\n"
        shift
    done
}
function get_packageversion_human_format {
    while :; do
        [ "$1" = "" ] && break
        name=$(get_packageversion_name $1)
        version=$(get_packageversion_version $1)
        if [ "$version" = "" ]; then
            printf "$name\n"
        else
            printf "$name@$version\n"
        fi
        shift
    done
}
