#!/bin/sh

snap list --color=never | awk '{if($6!="core" && $6 != "base") {print $1"@"$2}}' | tail -n +2
