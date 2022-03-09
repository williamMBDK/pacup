#!/bin/bash

SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

$SCRIPT_DIR/get-cache.sh

cachedir="$HOME/.cache/pacup/nix"

installed_packages=$(nix-env -q --json | jq -r '.[] | .pname + "@" + .version')

python - <<EOF
import json

file = open("$cachedir/packagecache.json", "r")
data = json.load(file)
file.close()

pacmap = {}

def insert(key, attrpath):
    if key in pacmap:
        l=len(pacmap[key])
        if l > len(attrpath):
            pacmap[key] = attrpath
    else:
        pacmap[key] = attrpath

for attrpath in data:
    pname = data[attrpath]['pname']
    version = data[attrpath]['version']
    insert((pname,version), attrpath)
    insert(pname, attrpath)

installed_packages=[tuple(p.split("@")) for p in """$installed_packages""".split()]
for pac in installed_packages:
    if pac in pacmap:
        print(pacmap[pac]+"@notsupported")
    elif pac[0] in pacmap:
        print(pacmap[pac]+"@notsupported")
    else:
        print("error: ", pac)
EOF

# nix-env -q --json | jq -r '.[] | .pname + "@" + .version'
