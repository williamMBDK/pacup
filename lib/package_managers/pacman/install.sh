#!/bin/bash

if [ "$#" -eq 2 ]; then
    echo "version not supported by pacman"
    exit 2
else
    sudo pacman --noconfirm --color always --asexplicit -S "$1" || exit 1
fi
