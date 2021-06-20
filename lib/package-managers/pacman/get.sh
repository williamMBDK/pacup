#!/bin/sh
pacman -Qne --color never | awk '{print $1"@"$2}' # only from sync databases
