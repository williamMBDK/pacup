#!/bin/sh
yay -Qe --color never | awk '{print $1"@"$2}'
