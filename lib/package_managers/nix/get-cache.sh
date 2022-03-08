#!/bin/bash

cachedir="$HOME/.cache/pacup/nix"

if ! [[ $(find "$cachedir/packagecache.json" -newermt '-60 minutes' 2>/dev/null) == "" ]]; then
    exit
fi

echo "Downloading nix package cache..."

mkdir -p $cachedir

nix-env -qaP --json > $cachedir/packagecache.json
