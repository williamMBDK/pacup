#!/bin/bash

if [ "$#" -eq 2 ]; then
    echo "version not supported by yay"
    exit 1
else
    yay --noconfirm --asexplicit -S "$1"
fi
