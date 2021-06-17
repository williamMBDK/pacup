#!/bin/sh

ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))/.."

if [[ -z "${PACUP_LISTS_DIR}" ]]; then
    PACUP_LISTS_DIR="~/.config/pacup/lists/"
fi

if [[ -z "${PACUP_CONFIGS_DIR}" ]]; then
    PACUP_CONFIGS_DIR="~/.config/pacup/configs/"
fi
