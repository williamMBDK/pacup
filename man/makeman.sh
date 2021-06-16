#!/bin/sh

SCRIPT_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pod2man -n pacup --release="1.0" -c "User Commands" $SCRIPT_DIR/man.pod > $SCRIPT_DIR/pacback.1
man $SCRIPT_DIR/pacback.1 > $SCRIPT_DIR/pacback.txt
