#!/bin/sh
# this does not entirely work, ii prints local packages that are not dependencies of other packages
pip list --user --not-required | awk '{print $1"@"$2}' | tail -n +3
