#!/bin/sh

SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pod2man -n pacup --release="1.0" -c "User Commands" $SCRIPT_DIR/man.pod > $SCRIPT_DIR/pacup.1
man $SCRIPT_DIR/pacup.1 > $SCRIPT_DIR/pacup.txt
