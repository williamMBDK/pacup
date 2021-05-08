#!/bin/sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel

SUBCMD=$1

case $SUBCMD in
    list)
        shift
        $SCRIPT_DIR/../lib/list.sh "$@"
        ;;
    *)
        show_help
        ;;
esac
