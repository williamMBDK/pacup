#!/bin/sh
lines=$(pacman -Qne --color never) # only from sync databases
echo "$lines" | while read line; do
    package="$(echo $line | cut -d ' ' -f1)"
    version="$(echo $line | cut -d ' ' -f2)"
    echo "p:$package, v:$version"
done
