#!/bin/sh

apm list --installed --bare | awk -F '@' '{print $1"@"$2}'
