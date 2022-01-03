from pathlib import Path
from .util.io import print_additional_info, lazy_confirm, print_needed_info, print_normal, print_success, print_warning
from .package_managers import get_package_managers

def handler(args):
    pms = get_package_managers_to_use(args)
    print_normal()
    generate_config_files(args, pms)
    print_normal()
    generate_list_files(args, pms)

def get_package_managers_to_use(args):
    pms = get_package_managers()
    pms_to_use = []
    for pm in pms:
        if not pm.is_installed():
            if args.verbosity >= 2:
                print_additional_info(
                    "{} is supported, but not installed. Skipping"
                    .format(pm.name)
                )
            continue
        if lazy_confirm("Do you wish to use {} with pacup?".format(pm.name)):
            pms_to_use.append(pm)
            print_success("Config file and package-list will be generated for {}".format(pm.name))
        else:
            print_additional_info("Skipping {}".format(pm.name))
    return pms_to_use

def generate_config_files(args, pms):
    configs_dir=Path(args.configs_dir)
    print_needed_info("GENERATING CONFIG FILES")
    print_needed_info("Using directory: {}".format(configs_dir))
    configs_dir.mkdir(parents=True, exist_ok=True)
    for pm in pms:
        filename=configs_dir.joinpath("{}.conf".format(pm.name))
        if filename.exists():
            print_warning("File already exists ({}). Skipping config generation for {}.".format(filename, pm.name))
        else:
            print_needed_info("Generating config file for {}: {}".format(pm.name, filename))
            with filename.open(mode="w") as f:
                f.write("+ all")
            print_success("Created file: {}".format(filename))

def generate_list_files(args, pms):
    lists_dir=Path(args.lists_dir)
    print_needed_info("GENERATING PACKAGE-LIST FILES")
    print_needed_info("Using directory: {}".format(lists_dir))
    lists_dir.mkdir(parents=True, exist_ok=True)
    for pm in pms:
        filename=lists_dir.joinpath("{}.list".format(pm.name))
        if filename.exists():
            print_warning("File already exists ({}). Skipping list generation for {}.".format(filename, pm.name))
        else:
            print_needed_info("Generating package-list file for {}: {}".format(pm.name, filename))
            print_needed_info("Backing up existing manually installed {} packages into {}".format(pm.name, filename))
            # TODO call backup
            print_success("Backup complete: pacup backup -qy -l {} {}".format(filename, pm.name))
