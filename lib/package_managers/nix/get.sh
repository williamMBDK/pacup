#!/bin/bash

nix profile list | awk {'print $2'} | awk -F '#' {'print $2'} | awk 'NF' | awk {'print $0"@unsupported"'}
