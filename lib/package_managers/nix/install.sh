#!/bin/bash

if [ "$#" -eq 2 ]; then
    nix-env -i $1-$2 || exit 1
else
    nix-env -i $1 || exit 1
fi
