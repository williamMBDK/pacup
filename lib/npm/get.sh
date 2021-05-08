#!/bin/bash
regex="(\+--|\`--|└──|├──) (.*)@(.*)"
output=$(npm list -g -depth=0 | tail -n +2 | head -n -1)
echo "$output" | while read line ; do
	[[ $line =~ $regex ]]
	package="${BASH_REMATCH[2]}"
	version="${BASH_REMATCH[3]}"
	echo p:$package, v:$version
done
