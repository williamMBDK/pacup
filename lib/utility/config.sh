#!/bin/sh

ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))/.."

if [[ -z "${PACUP_LISTS_DIR}" ]]; then
    PACUP_LISTS_DIR=~/.config/pacup/lists
fi

if [[ -z "${PACUP_CONFIGS_DIR}" ]]; then
    PACUP_CONFIGS_DIR=~/.config/pacup/configs
fi

function get_lists_dir {
    printf "$PACUP_LISTS_DIR"
}

function get_configs_dir {
    printf "$PACUP_CONFIGS_DIR"
}

function get_list_for_package_manager {
    printf "$(get_lists_dir)/$1"
}

function get_config_for_package_manager {
    printf "$(get_configs_dir)/$1"
}
