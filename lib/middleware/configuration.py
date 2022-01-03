from ..configuration import get_configs_dir, get_lists_dir
from ..configuration import ConfigurationFactory, TaggedPackageListFactory
from ..util.io import print_warning

def add_config_argument(parser):
    parser.add_argument(
        "-c", "--config"
    )

# depends on args.package_managers
def config_middleware(args):
    assert(hasattr(args, "config"))
    if args.config != None and \
       hasattr(args, "package_managers") and \
       len(args.package_managers) > 1:
        print_warning("ignoring -c/--config since multiple package managers were specified")
        args.config = None

def add_list_argument(parser):
    parser.add_argument(
        "-l", "--list"
    )

# depends on args.package_managers
def list_middleware(args):
    assert(hasattr(args, "list"))
    if args.list != None and \
       hasattr(args, "package_managers") and \
       len(args.package_managers) > 1:
        print_warning("ignoring -l/--list since multiple package managers were specified")
        args.list = None

# depends on:
    # args.package_managers, also modifies this
    # args.config
    # args.verbosity
def load_configs(args):
    assert(hasattr(args, "package_managers"))
    new_package_managers = []
    for pm in args.package_managers:
        if args.config != None:
            pm.set_config(ConfigurationFactory.create_configuration_from_filename(
                args.config))
            new_package_managers.append(pm)
        elif pm.has_config():
            pm.set_config(ConfigurationFactory.create_configuration_from_filename(
                pm.get_config_path()))
            new_package_managers.append(pm)
        else:
            if args.verbosity >= 2:
                print_warning(
                    "ignoring package-manager {} as it does not have a configuration file: {}"
                    .format(pm.name, pm.get_config_path())
                )
    args.package_managers = new_package_managers

# depends on:
    # args.package_managers, also modifies this
    # args.list
    # args.verbosity
def load_lists(args):
    assert(hasattr(args, "package_managers"))
    new_package_managers = []
    for pm in args.package_managers:
        if args.list != None:
            pm.set_list(TaggedPackageListFactory.create_list_from_filename(
                args.list))
            new_package_managers.append(pm)
        elif pm.has_list():
            pm.set_list(TaggedPackageListFactory.create_list_from_filename(
                pm.get_list_path()))
            new_package_managers.append(pm)
        else:
            if args.verbosity >= 2:
                print_warning(
                    "ignoring package-manager {} as it does not have a list file: {}"
                    .format(pm.name, pm.get_lsit_path())
                )
    args.package_managers = new_package_managers

def add_configs_dir_argument(parser):
    parser.add_argument(
        "-c", "--configs-dir",
        dest="configs_dir",
        default=get_configs_dir()
    )
    
def add_lists_dir_argument(parser):
    parser.add_argument(
        "-l", "--lists-dir",
        dest="lists_dir",
        default=get_lists_dir()
    )
