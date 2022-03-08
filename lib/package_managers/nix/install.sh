#!/bin/bash

if [ "$#" -eq 1 ]; then
    echo "version not supported by nix"
    exit 2
else
    nix-env -i $1 || exit 1
fi
