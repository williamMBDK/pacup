import os
from ..configuration import ConfigurationFactory, TaggedPackageListFactory, get_config_path, get_list_path
from ..util.output import print_warning

def add_config_argument(parser):
    parser.add_argument(
        "-c", "--config"
    )

# depends on args.package_managers
def add_config_middleware(middleware):
    def f(args):
        assert(hasattr(args, "config"))
        if args.config != None and \
           hasattr(args, "package_managers") and \
           len(args.package_managers) > 1:
            print_warning("ignoring -c/--config since multiple package managers were specified")
            args.config = None
    middleware.append(f)

def add_list_argument(parser):
    parser.add_argument(
        "-l", "--list"
    )

# depends on args.package_managers
def add_list_middleware(middleware):
    def f(args):
        assert(hasattr(args, "list"))
        if args.list != None and \
           hasattr(args, "package_managers") and \
           len(args.package_managers) > 1:
            print_warning("ignoring -l/--list since multiple package managers were specified")
            args.list = None
    middleware.append(f)

# depends on:
    # args.package_managers, also modifies this
    # args.config
def load_configs(middleware):
    def f(args):
        assert(hasattr(args, "package_managers"))
        new_package_managers = []
        for pm in args.package_managers:
            if args.config != None:
                pm.config = ConfigurationFactory.create_configuration_from_filename(args.config)
                new_package_managers.append(pm)
            elif os.path.exists(get_config_path(pm.name)):
                pm.config = ConfigurationFactory.create_configuration_from_config(pm.name)
                new_package_managers.append(pm)
            else:
                print_warning("ignoring package-manager {} as it does not have a configuration file: {}".format(pm.name, get_config_path(pm.name)))
        args.package_managers = new_package_managers
    middleware.append(f)

# depends on:
    # args.package_managers
    # args.list
def load_lists(middleware):
    def f(args):
        assert(hasattr(args, "package_managers"))
        new_package_managers = []
        for pm in args.package_managers:
            if args.list != None:
                pm.list = TaggedPackageListFactory.create_list_from_filename(args.list)
                new_package_managers.append(pm)
            elif os.path.exists(get_list_path(pm.name)):
                pm.list = TaggedPackageListFactory.create_list_from_config(pm.name)
                new_package_managers.append(pm)
            else:
                print_warning("ignoring package-manager {} as it does not have a list file: {}".format(pm.name, get_config_path(pm.name)))
        args.package_managers = new_package_managers
    middleware.append(f)
