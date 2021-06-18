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
    print_success "Created directory: mkdir -p $lists_dir"
    mkdir -p $lists_dir

    for package_manager in $(get_package_managers); do
        varname=${package_manager^^}
        if [ ${!varname} = 1 ]; then
            print_needed_info "Generating package-list file for $package_manager: $lists_dir/$package_manager.list"
            touch $lists_dir/$package_manager.list
            print_success "Created file: touch $lists_dir/$package_manager.list"
            print_needed_info "Backing up existing manually installed $package_manager packages into $lists_dir/$package_manager.list"
            $ROOTDIR/backup.sh -qy -p $package_manager -l "$lists_dir/$package_manager.list"
            print_success "Backup complete: pacup backup -qy -p $package_manager -l $lists_dir/$package_manager.list"
        fi
    done
else
    print_warning "Directory already exists ($lists_dir). Skipping list generation."
fi

echo

print_needed_info "GENERATING CONFIG FILES"
print_needed_info "Using directory: $configs_dir"
if ! [[ -d $configs_dir ]]; then
    print_success "Created directory: mkdir -p $configs_dir"
    mkdir -p $configs_dir

    for package_manager in $(get_package_managers); do
        varname=${package_manager^^}
        if [ ${!varname} = 1 ]; then
            print_needed_info "Generating config file for $package_manager: $configs_dir/$package_manager.conf"
            printf "+ all" > $configs_dir/$package_manager.conf
            print_success "Created file: printf \"+ all\" > $configs_dir/$package_manager.conf"
        fi
    done
else
    print_warning "Directory already exists ($configs_dir). Skipping config generation."
fi
