from .middleware.configuration import load_configs, load_lists, config_middleware, list_middleware
from .util.output import print_cyan, print_needed_info, print_green, print_warning, print_success, print_blue, print_normal
from .configuration import get_configs_dir, get_lists_dir
from .package_managers import PackageManager

def handler(args):
    status_of_user_configuration()
    print_normal("")
    status_of_package_managers(args)
    config_middleware(args)
    list_middleware(args)
    load_configs(args)
    load_lists(args)
    for pm in args.package_managers:
        print_normal("")
        status_of_packages_for_package_manager(pm)

def status_of_user_configuration():
    print_needed_info("STATUS OF USER CONFIGURATION")
    print_green("USER CONFIGS DIRECTORY: {}".format(get_configs_dir()))
    print_green("USER LISTS DIRECTORY: {}".format(get_lists_dir()))

def status_of_package_managers(args):
    print_needed_info("STATUS OF SUPPORTED PACKAGE MANAGERS")
    for pm in args.package_managers:
        pm : PackageManager = pm
        if not pm.is_installed():
            print_cyan("{} is not installed".format(pm.name))
        elif not pm.has_config() and not pm.has_list():
            print_cyan("{} is installed".format(pm.name))
        elif not pm.has_config():
            print_warning(
                "{} is installed and has a package list, but not a config"
                .format(pm.name)
            )
        elif not pm.has_list():
            print_warning(
                "{} is installed and has a config, but not a package list"
                .format(pm.name)
            )
        else:
            print_success(
                "{} is installed, has a package list and a config"
                .format(pm.name)
            )

def status_of_packages_for_package_manager(pm : PackageManager):
    print_needed_info("STATUS OF PACKAGES FOR {}".format(pm.name.upper()))
    matches = set(pm.get_config().get_matching_packages(pm.get_list()))
    for pac in matches:
        if not pm.is_package_installed(pac):
            print_warning("NOT INSTALLED OR NOT UP-TO-DATE: {}".format(pac))
    explicits = pm.get_installed_packages()
    for pac in explicits:
        if not pm.get_list().contains(pac) and \
           not pm.get_list().contains(pac.without_version()):
            print_cyan(
                "INSTALLED BUT NOT IN PACKAGE LIST: {}"
                .format(pac.without_version())
            )
        elif pac not in matches and \
             pac.without_version() not in matches:
            print_blue(
                "INSTALLED, IN PACKAGE LIST BUT NOT IN CONFIG: {}"
                .format(pac.without_version())
            )
