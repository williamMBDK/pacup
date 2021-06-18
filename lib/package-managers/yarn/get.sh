#!/bin/sh

dir=$(yarn global dir 2> /dev/null)
packages="$(jq -r '.dependencies | keys[]' $dir/package.json)"

IFS=$'\n'
for package in $packages; do
    pacdir="$dir/node_modules/$package"
    version="$(jq -r '.version' $pacdir/package.json)"
    echo "$package $version"
done
