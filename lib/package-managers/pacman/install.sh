#!/bin/sh
if [ "$#" -eq 2 ]; then
    echo "version not supported by pacman"
    exit 1
else
    sudo pacman --asexplicit -S "$1"
fi
