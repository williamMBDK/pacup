#!/bin/sh
package=$1
version=$2
if [ "$#" -eq 2 ]; then
    echo "versioned installation of snaps not supported by pacup yet"
    exit 1
else
    sudo snap install "$package"
fi
