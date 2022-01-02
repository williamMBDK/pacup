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

def setup_parser_backup(parser : argparse.ArgumentParser, middleware):
    parser.set_defaults(handler=backup.handler)

def setup_parser_check(parser, middleware):
    parser.set_defaults(handler=check.handler)
    # arguments
    add_common_arguments(parser)
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
    parser.set_defaults(handler=list.handler)

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
