import argparse
from . import backup
from . import check
from . import clear_cache
from . import generate_config
from . import install
from . import list_subcommand
from . import status

def setup_parser_backup(parser):
    parser.set_defaults(handler=backup.handler)

def setup_parser_check(parser):
    parser.set_defaults(handler=check.handler)

def setup_parser_clear_cache(parser):
    parser.set_defaults(handler=clear_cache.handler)

def setup_parser_generate_config(parser):
    parser.set_defaults(handler=generate_config.handler)

def setup_parser_install(parser):
    parser.set_defaults(handler=install.handler)

def setup_parser_list(parser):
    parser.set_defaults(handler=list_subcommand.handler)

def setup_parser_status(parser):
    parser.set_defaults(handler=status.handler)

def create_parser():
    parser = argparse.ArgumentParser(prog="pacup")

    ### subcommands ###
    subparsers = parser.add_subparsers()

    parser_backup = subparsers.add_parser('backup')
    setup_parser_backup(parser_backup)

    parser_check = subparsers.add_parser('check')
    setup_parser_check(parser_check)

    parser_clear_cache = subparsers.add_parser('clear-cache')
    setup_parser_clear_cache(parser_clear_cache)

    parser_generate_config = subparsers.add_parser('generate-config')
    setup_parser_generate_config(parser_generate_config)

    parser_install = subparsers.add_parser('install')
    setup_parser_install(parser_install)

    parser_list = subparsers.add_parser('list')
    setup_parser_list(parser_list)

    parser_status = subparsers.add_parser('status')
    setup_parser_status(parser_status)

    return parser
