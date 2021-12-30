#!/bin/bash

apm list --installed --bare | awk -F '@' '{print $1"@"$2}'
