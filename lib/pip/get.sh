regex="(.*)==(.*)"
list=( $(pip freeze --user) )
for item in ${list[@]}; do
	[[ $item =~ $regex ]]
	package="${BASH_REMATCH[1]}"
	version="${BASH_REMATCH[2]}"
	echo p:$package, v:$version
done
