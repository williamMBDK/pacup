#!/bin/sh
package=$1
version=$2
if [ "$#" -eq 2 ]; then
    yarn global add "$package@$version"
else
    yarn global add "$package"
fi
