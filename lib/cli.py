import argparse, os
from . import backup
from . import check
from . import clear_cache
from . import generate_config
from . import install
from . import list_subcommand
from . import status
from .package_managers import valid_package_manager_names, package_managers, PackageManager
from .util.output import print_warning
from .configuration import ConfigurationFactory, TaggedPackageListFactory, get_config_path, get_list_path

class _PackageManagerSetAction(argparse.Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if values == "all" or "all" in values:
            values = valid_package_manager_names
        values = set(values)
        pms = list(filter(lambda pm: pm.name in values, package_managers))
        setattr(namespace, self.dest, pms)

def add_package_managers_argument(parser):
    # 'all' is a hack to fix this bug: https://bugs.python.org/issue41047
    parser.add_argument(
        "package_managers",
        nargs="*",
        choices=valid_package_manager_names + ["all"], 
        action=_PackageManagerSetAction,
        help="package manager: {}".format(", ".join(valid_package_manager_names)),
        default="all",
        metavar="package-manager",
    )

def add_package_managers_middleware(middleware):
    def f(args):
        assert(hasattr(args, "package_managers"))
        new_packages_managers = []
        for pm in args.package_managers:
            pm : PackageManager = pm
            if not pm.is_installed():
                print_warning("ignoring package-manager {} as it is not installed".format(pm.name))
                continue
            new_packages_managers.append(pm)
        args.package_managers = new_packages_managers
    middleware.append(f)

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

def setup_parser_backup(parser : argparse.ArgumentParser, middleware):
    parser.set_defaults(handler=backup.handler)
    #parser.add_argument("-l", "--package-list")

def setup_parser_check(parser, middleware):
    parser.set_defaults(handler=check.handler)
    # arguments
    add_package_managers_argument(parser)
    add_config_argument(parser)
    add_list_argument(parser)
    # middleware
    add_package_managers_middleware(middleware)
    add_config_middleware(middleware)
    add_list_middleware(middleware)
    load_configs(middleware)
    load_lists(middleware)

def setup_parser_clear_cache(parser, middleware):
    parser.set_defaults(handler=clear_cache.handler)

def setup_parser_generate_config(parser, middleware):
    parser.set_defaults(handler=generate_config.handler)

def setup_parser_install(parser, middleware):
    parser.set_defaults(handler=install.handler)

def setup_parser_list(parser, middleware):
    parser.set_defaults(handler=list_subcommand.handler)

def setup_parser_status(parser, middleware):
    parser.set_defaults(handler=status.handler)

def create_parser():
    parser = argparse.ArgumentParser(prog="pacup")
    middleware = []

    ### subcommands ###
    subparsers = parser.add_subparsers()

    parser_backup = subparsers.add_parser('backup')
    setup_parser_backup(parser_backup, middleware)

    parser_check = subparsers.add_parser('check')
    setup_parser_check(parser_check, middleware)

    parser_clear_cache = subparsers.add_parser('clear-cache')
    setup_parser_clear_cache(parser_clear_cache, middleware)

    parser_generate_config = subparsers.add_parser('generate-config')
    setup_parser_generate_config(parser_generate_config, middleware)

    parser_install = subparsers.add_parser('install')
    setup_parser_install(parser_install, middleware)

    parser_list = subparsers.add_parser('list')
    setup_parser_list(parser_list, middleware)

    parser_status = subparsers.add_parser('status')
    setup_parser_status(parser_status, middleware)

    return parser, middleware
