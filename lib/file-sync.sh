#!/bin/sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel

source $SCRIPT_DIR/util.sh

PACSYNC_CONFIGS=~/pacback-configs

if [ ! -d $PACSYNC_CONFIGS ]; then
    config_path_not_exist $PACSYNC_CONFIGS
    exit 1
fi

ALL=0

QUIET=0
VERBOSE=0

for package_manager in $(get_package_managers); do
    eval "$package_manager=0"
done

# https://gist.github.com/deshion/10d3cb5f88a21671e17a
while :; do
    case $1 in
        -h|-\?|--help)
            showhelp
            exit
            ;;
        -q|--quiet)
            QUIET=1
            ;;
        -v|--verbose)
            VERBOSE=1
            ;;
        all)
            ALL=1
            ;;
        apt|yay|npm|pacman|pip|yarn)
            eval "$1=1"
            ;;
        #get_package_manager_pattern)
        #    eval "$1=1"
        #    ;;
        -?*)
            wrong_option $1
            ;;
        --?*)
            wrong_option $1
            ;;
        "")
            break
            ;;
        *)
            wrong_package_manager $1
            ;;
    esac
    shift
done

function process {
    package_manager=$1
    config_file="$PACSYNC_CONFIGS/$package_manager.conf"
    if [ ! -f $config_file ]; then
        echo "Config file does not exist: $config_file"
        echo "Creating config file: $config_file"
        touch $config_file
    fi
}

for package_manager in $(get_package_managers); do
    if test ${!package_manager} -eq 1 ; then
        process $package_manager
    fi
done

# difference=$(diff -U 0 --color=always ~/arch-setup/yay/packages.txt ~/arch-setup/yay/temp-packages.txt | tail -n +4)
# mv ~/arch-setup/yay/temp-packages.txt ~/arch-setup/yay/packages.txt
# if [[ $difference = *[![:space:]]* ]]
# then
# 	echo "Synced packages from yay with local file"
# 	echo $difference
# else
# 	echo "Nothing to sync"
# fi
# 
