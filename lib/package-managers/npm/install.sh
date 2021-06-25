#!/bin/bash

package=$1
version=$2
if [ "$#" -eq 2 ]; then
    sudo npm install -g "$package@$version"
else
    sudo npm install -g "$package"
fi
