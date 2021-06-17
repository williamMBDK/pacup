# PacUp
Back**up** of lists of explicitly installed **pac**kages from various linux package managers

Note: PacUp currently does not support any of the below features besides listing explicitly installed packages.

# Installation
Since PacUp manages package managers PacUp is not accessible in any package manager. Instead simply clone this repo and run the `path/to/pacup-repo/bin/pacup.sh` shell script.

```shell
git clone https://github.com/williamMBDK/pacup.git
```

You may optionally add `path/to/pacup-repo/bin` to your path and then the command `pacup` will be accessible.
```shell
export PATH="/path/to/pacup-repo/bin:$PATH"
```

# The (initial) concept 
You will create a config file for each of your package managers.
A config file will contain a list of package configurations, consisting of a package name, an optional version number and a list of tags. By default each package configuration will have the *all* tag, and a unique tag which is *package@version* (or *package* if version is not specified).
Creating a config file for a given package manager is easy since PacUp has built in features to generate and maintain them - however it is meant for you to do some manual editing of the config files (adding tags...).

Then you should use github or any other git host to backup your config files (or another way of backing up the config files).

Then on each of your linux machines (desktop, laptop, work computer, server, ...) you can simply pull the config files and install the packages it specifies using PacUp. Optionally you can create a machine specific config file, where you for each package managers specify which tags should be installed (or more precisely for each specified tag the corresponding package configuration will be installed). You can also specify tags that should not be installed (these will take presedence). Then PacUp will install only those package configurations specified by the tags. For example you could have *dev* tag specifying packages used for software development, and only have these dev packages be installed on you work machine and laptop.

When you wish to add a new package you can either manually add it to a config file or install it and then sync to the config file.

PacUp is very interactive and will handle all sorts of edge cases with duplicated packages, inconsistent versions, error resolution and so on (todo).

# Features
* Configuration files for many different package managers.
    * List of packages
    * Optional version numbers
* Create specific configurations for each linux machine using tagged packages.
* Automated configuration management.
* Optionally very interactive.
* Has built-in commands for listing explicitly installed packages for many package managers.
* Currently supports the following package managers:
    * apt
    * npm (*global*)
    * pacman
    * pip (*global*)
    * yarn (*global*)
    * yay

    More will be added.

    Here *global* refers to the global installation of packages, since some of these package managers can be used for project package management.
* Compatible with the POSIX shell specification (todo), and can thus run on nearly any linux distribution (todo: does there exist distros it cannot run on?)

# Configuration 
## Package manager config files
This is the config files that specifies the list of package configurations for each of your package managers.
### Location
Todo
### Format
Todo
* Can contain duplicate packages (packages with different versions).
## Machine specific config files
This is the configuration files that specifies which packages a specific linux machine should have installed for each package manager.
### Location
Todo
### Format
Todo
* Cannot contain duplicate packages.

# Contributing
Feel free to contribute.

I especially need advice and help on testing the shell code, which I think will be quite inconvenient.

\- William

## todo
- PacUp status default all
- name: pacup* or packup??
- script for each packagemanager that prints what features are available
- what if a newer version of a match is installed and we try to install the match?
- version optional in list script, and status script
- is $IFS handled correctly everywhere?
- many different package managers in backup, status and so on
