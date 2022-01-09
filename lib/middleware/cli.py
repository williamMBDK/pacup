import argparse
from .. import backup
from .. import check
from .. import clear_cache
from .. import generate_config
from .. import install
from .. import list
from .. import status
from .configuration import *
from .package_managers import *
from .middleware import setup_middleware, add_middleware

def add_common_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.set_defaults(verbosity=1)
    group.add_argument(
        "-q", "--quiet",
        action="store_const",
        const=0,
        dest="verbosity"
    )
    group.add_argument(
        "-v", "--verbose",
        action="store_const",
        const=2,
        dest="verbosity"
    )

def add_with_version_argument(parser):
    parser.add_argument(
        "-V", "--with-version",
        dest="with_version",
        action="store_true",
        default=False
    )

def add_yes_argument(parser):
    parser.add_argument(
        "-y", "--yes",
        dest="yes",
        action="store_true",
        default=False
    )

def setup_parser_backup(parser : argparse.ArgumentParser):
    setup_middleware(parser)
    parser.set_defaults(handler=backup.handler)
    # arguments
    add_common_arguments(parser)
    add_package_managers_argument(parser)
    add_list_argument(parser)
    add_with_version_argument(parser) 
    # TODO these should not both be there??
    add_yes_argument(parser) 
    parser.add_argument(
        "-i", "--interactive",
        dest="interactive",
        action="store_true",
        default=False
    )
    # middleware
    add_middleware(parser, add_package_managers_conversion_middleware)
    add_middleware(parser, add_package_managers_is_installed_middleware)
    add_middleware(parser, list_middleware)
    add_middleware(parser, load_lists)

def setup_parser_check(parser):
    setup_middleware(parser)
    parser.set_defaults(handler=check.handler)
    # arguments
    add_common_arguments(parser)
    add_package_managers_argument(parser)
    add_config_argument(parser)
    add_list_argument(parser)
    # middleware
    add_middleware(parser, add_package_managers_conversion_middleware)
    add_middleware(parser, add_package_managers_is_installed_middleware)
    add_middleware(parser, config_middleware)
    add_middleware(parser, list_middleware)
    add_middleware(parser, load_configs)
    add_middleware(parser, load_lists)

def setup_parser_clear_cache(parser):
    setup_middleware(parser)
    parser.set_defaults(handler=clear_cache.handler)
    # arguments
    add_common_arguments(parser)

def setup_parser_generate_config(parser):
    setup_middleware(parser)
    parser.set_defaults(handler=generate_config.handler)
    # arguments
    add_common_arguments(parser)
    add_configs_dir_argument(parser)
    add_lists_dir_argument(parser)

def setup_parser_install(parser):
    setup_middleware(parser)
    parser.set_defaults(handler=install.handler)
    # arguments
    add_common_arguments(parser)
    add_package_managers_argument(parser)
    add_config_argument(parser)
    add_list_argument(parser)
    add_yes_argument(parser)
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        default=False
    )
    # middleware
    add_middleware(parser, add_package_managers_conversion_middleware)
    add_middleware(parser, add_package_managers_is_installed_middleware)
    add_middleware(parser, config_middleware)
    add_middleware(parser, list_middleware)
    add_middleware(parser, load_configs)
    add_middleware(parser, load_lists)

def setup_parser_list(parser : argparse.ArgumentParser):
    setup_middleware(parser)
    parser.set_defaults(handler=list.handler)
    # arguments
    add_common_arguments(parser)
    add_package_managers_argument(parser)
    # TODO these two could be in a mutually exclusive group?
    add_with_version_argument(parser) 
    parser.add_argument(
        "-c", "--count",
        dest="perform_count",
        action="store_true",
        default=False
    )
    # middleware
    add_middleware(parser, add_package_managers_conversion_middleware)
    add_middleware(parser, add_package_managers_is_installed_middleware)

def setup_parser_status(parser):
    setup_middleware(parser)
    parser.set_defaults(handler=status.handler)
    # arguments
    add_common_arguments(parser)
    add_package_managers_argument(parser)
    add_config_argument(parser)
    add_list_argument(parser)
    # middleware
    add_middleware(parser, add_package_managers_conversion_middleware)

EPILOG="developed by William Bille Meyling"

def create_parser():
    parser = argparse.ArgumentParser(
        prog="pacup",
        description="backup lists of explicitly installed packages from various linux package managers.",
        epilog=EPILOG,
        allow_abbrev=False
    )
    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0',
        help="Show the pacup version and exit"
    )

    ### subcommands ###
    subparsers = parser.add_subparsers(
        description="pacup has the following subcommands available. all relevant subcommands allow the names of package managers to be given as positional arguments, and only apply the operation for the given package managers.",
        metavar="command",
    )

    parser_backup = subparsers.add_parser(
        'backup',
        epilog=EPILOG,
        help="add packages not in the package-list to the package list",
    )
    setup_parser_backup(parser_backup)

    parser_check = subparsers.add_parser(
        'check',
        epilog=EPILOG,
        help="show which packages from the package-list are matched by the configuraion file",
    )
    setup_parser_check(parser_check)

    parser_clear_cache = subparsers.add_parser(
        'clear-cache',
        epilog=EPILOG,
        help="clear cache used by pacup",
    )
    setup_parser_clear_cache(parser_clear_cache)

    parser_generate_config = subparsers.add_parser(
        'generate-config',
        epilog=EPILOG,
        help="generate package-lists and configuration files from what is currently installed"
    )
    setup_parser_generate_config(parser_generate_config)

    parser_install = subparsers.add_parser(
        'install',
        epilog=EPILOG,
        help="install packages specified by a configuration file (and the corresponding package-list)"
    )
    setup_parser_install(parser_install)

    parser_list = subparsers.add_parser(
        'list',
        epilog=EPILOG,
        help="list explicitly installed packages (installed directly by user)"
    )
    setup_parser_list(parser_list)

    parser_status = subparsers.add_parser(
        'status',
        epilog=EPILOG,
        help="show the current status of the pacup configuration (packages that are not backed up / installed and more)"
    )
    setup_parser_status(parser_status)

    return parser
