#!/bin/bash
packages=( $(comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u)) )
for package in ${packages[@]}; do
	version=$(apt-cache show $package | grep "Version" | head -n 1)
	echo "p:$package, v:$version"
done
