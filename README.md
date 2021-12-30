# PacUp
Back**up** of lists of explicitly installed **pac**kages from various linux package managers

## TLDR
Create a 'package-list' for each package-manager, and a 'config' for each package-manager on each linux machine. The configs describes which packages from the 'package-lists' should be installed on a specific machine.

# Prerequisites
* python3
* bash (only tested in bash for now)
* (optional) [argcomplete](https://github.com/kislyuk/argcomplete) (for bash autocomplete)

# Installation
Since PacUp manages package managers PacUp is not (atm) accessible in any package manager. Instead simply clone this repo and the `path/to/pacup-repo/bin/pacup` python script is the entrypoint for the program.

```shell
git clone https://github.com/williamMBDK/pacup.git
```

You may optionally add `path/to/pacup-repo/bin` to your path and then the command `pacup` will be accessible.
```shell
export PATH="/path/to/pacup-repo/bin:$PATH"
```

To get bash autocompletion you should install [argcomplete](https://github.com/kislyuk/argcomplete). Then you either enable argcomplete globally or source the following script.
```
source /path/to/pacup-repo/completion/pacup-completion
```

# The concept 
PacUp aims to make it easier to synchronize or move a linux setup from one machine to another. A big part of this is to install packages from package-managers. PacUp helps automate this through 'package-lists' and local 'configurations' (explained below).

A 'package-list' is part of the PacUp user configuration, and it contains a list of all the packages a user has across all of the users machines. Moreover, each package manager that the user uses has a seperate 'package-list'. Entries in a 'package-list' consists of a package name, an optional version number and a list of tags. Creating a 'package-list' file for a given package manager is easy since PacUp has built in functionality to generate and maintain them - however it is meant for you to do some manual editing of the 'package-lists' (adding tags and so on).

On each of the user's machines the user then creates a local 'configuration' (or config) for each chosen package manager. A config describes which packages from a corresponding 'package-list' should be installed on the specific machine. In the config file the user can specify to include/exclude specific packages or specific tags. For example you could have a *dev* tag specifying packages used for software development, and only have these *dev* packages be installed on you work machine.

It is recommended to use github or any other git host to backup your 'package-list' files, such that they can easily be accessed on a new machine.

Initially you can use `pacup generate-config` to generate starting configuration files, which will be placed in `~/.config/pacup`.

# Highlighted Features
* Easy to use using the status subcommand, which gives an overview of the current configuration for all package-managers, and the install subcommand which installs all the packages that are specified by the configs for all package managers.
* Create specific configurations for each Linux machine using tagged packages.
* Automated configuration management.
    * Backup newly installed packages into the 'package-lists' (backup)
    * Validate the correctness of the configuration (check)
    * Generate initial configuration files (generate-config)
* Built-in commands for listing explicitly installed packages for many package managers.
* Supported package managers:
    * apm
    * apt
    * npm
    * pacman
    * pip
    * snap
    * yarn
    * yay
* Upcoming: Compatible with the POSIX shell specification, and can thus run on nearly any linux distribution.

# Configuration 
## Package-lists
### Location
### Format
* Can contain duplicate packages (the same package but with different versions).
## Configurations (configs)
The configuration files that specify which packages a specific Linux machine should have installed for each chosen package manager.
### Location
### Format
* Cannot contain duplicate packages.

# Support for additional package managers

# Contributing
Feel free to contribute.

\- William

## TODO
- PacUp status default all
- script for each packagemanager that prints what features are available
- what if a newer version of a match is installed and we try to install the match?
- use local
- make global variables used in other functions, ex. QUIET be prefixed by PACUP
- yes option for install
- make all not include stuff that does not have config/lists I think
- bash completion
- check correct output for -q. not newlines...
- make code nicer
- write readme
    - mention completion
- when using string comparison use quotes
- use proper comparison methods for different things ex. (( vs [[
- divide util.sh into differnet files???
- spacing in list script output
- user defined package managers - a pm wrapper for config files
- add check for duplicate pm in get_package_managers for EXTRA_PMS
- -y option for install script
- fix that -l and -c are not able to be used unless the given package manager already has a config/list in the default location
- remove IFS everywhere
- yarn file does not exist initially when no other packages are installed
- flush io install script such that you dont accidentally accept by pressing enter before a question arises

# IDEAS
- Config file combined for all package managers?
- Uninstall script?
- Ignored packages (ex. packages that are already installed explicitely in kali)
