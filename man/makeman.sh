#!/bin/sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel

pod2man -n pachey -d hey -c test $SCRIPT_DIR/man.pod > $SCRIPT_DIR/pacback.1
man $SCRIPT_DIR/pacback.1 > $SCRIPT_DIR/pacback.txt
