#!/bin/sh
regex="^info \"(.*)@(.*)\""
items=$(yarn global list 2> /dev/null | grep -P "info")
echo "$items" | while read line ; do
	[[ $line =~ $regex ]]
	package="${BASH_REMATCH[1]}"
	version="${BASH_REMATCH[2]}"
	echo p:$package, v:$version
done
