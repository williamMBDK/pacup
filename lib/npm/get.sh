regex="(└──|├──) (.*)@(.*)"
output=$(npm list -g --depth=0 | tail -n 3 | head -n 2)
echo "$output" | while read line ; do
	[[ $line =~ $regex ]]
	echo $line
	package="${BASH_REMATCH[2]}"
	version="${BASH_REMATCH[3]}"
	echo p:$package, v:$version
done
