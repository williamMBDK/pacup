#!/bin/sh
lines=$(yay -Qe --color never)
echo "$lines" | while read line; do
    package="$(echo $line | cut -d ' ' -f1)"
    version="$(echo $line | cut -d ' ' -f2)"
    echo "$package $version"
done
