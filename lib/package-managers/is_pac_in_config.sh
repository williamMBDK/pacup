matches=$1
packageandversion=$2
package=$(echo $packageandversion  | head -n1 | cut -d " " -f1)

if ! printf "$matches" | grep "^$packageandversion$" > /dev/null && ! printf "$matches" | grep "^$package$" > /dev/null; then
    exit 1
fi
exit 0
