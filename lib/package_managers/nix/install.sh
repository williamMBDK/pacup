#!/bin/bash

if [ "$#" -eq 2 ]; then
    echo "version not supported by nix"
    exit 2
else
    NIXPKGS_ALLOW_UNFREE=1 \
        nix profile install --impure nixpkgs#$1 || exit 1
fi
