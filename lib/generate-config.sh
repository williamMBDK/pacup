#!/bin/sh

# imports
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/util.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
source $ROOTDIR/utility/config.sh
ROOTDIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"

lists_dir=$(get_lists_dir)
configs_dir=$(get_configs_dir)

print_needed_info "PACKAGE MANAGER SELECTION"
for package_manager in $(get_package_managers); do
    declare -g "${package_manager^^}=0"
    if ! does_package_manager_exist "$package_manager"; then
        print_additional_info "$package_manager is supported but not installed. Skipping."
        continue
    fi
    if lazy_confirm "Do you wish to use $package_manager with pacup?"$; then
        declare -g "${package_manager^^}=1"
        print_success "Package-list and config files wil be generated for $package_manager"
    else
        print_additional_info "Skipping $package_manager"
    fi
done

echo

print_needed_info "GENERATING PACKAGE LISTS FILES"
print_needed_info "Using directory: $lists_dir"
if ! [[ -d $lists_dir ]]; then
    mkdir -p $lists_dir
    print_success "Created directory: mkdir -p $lists_dir"
fi
for package_manager in $(get_package_managers); do
    filename="$lists_dir/$package_manager.list"
    varname=${package_manager^^}
    if [ ${!varname} = 1 ]; then
        if ! [ -e "$filename" ]; then
            print_needed_info "Generating package-list file for $package_manager: $filename"
            touch $filename
            print_success "Created file: touch $filename"
            print_needed_info "Backing up existing manually installed $package_manager packages into $filename"
            $ROOTDIR/backup.sh -qy -l "$filename" $package_manager
            print_success "Backup complete: pacup backup -qy -l $filename $package_manager"
        else
            print_warning "File already exists ($filename). Skipping list generation for $package_manager."
        fi
    fi
    
done

echo

print_needed_info "GENERATING CONFIG FILES"
print_needed_info "Using directory: $configs_dir"
if ! [[ -d $configs_dir ]]; then
    print_success "Created directory: mkdir -p $configs_dir"
    mkdir -p $configs_dir
fi
for package_manager in $(get_package_managers); do
    filename="$configs_dir/$package_manager.conf"
    varname=${package_manager^^}
    if [ ${!varname} = 1 ]; then
        if ! [ -e "$filename" ]; then
            print_needed_info "Generating config file for $package_manager: $filename"
            printf "+ all" > $filename
            print_success "Created file: printf \"+ all\" > $filename"
        else
            print_warning "File already exists ($filename). Skipping config generation for $package_manager."
        fi
    fi
done
