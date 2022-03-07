#!/bin/bash

nix-env -q --json | jq -r '.[] | .pname + "@" + .version'
