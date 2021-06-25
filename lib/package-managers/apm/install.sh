#!/bin/bash

package=$1
version=$2
if [ "$#" -eq 2 ]; then
    apm install "$package@$version"
else
    apm install "$package"
fi
