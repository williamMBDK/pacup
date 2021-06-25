#!/bin/bash

if [ "$#" -eq 2 ]; then
	sudo apt install $1=$2
else
	sudo apt install $1
fi
