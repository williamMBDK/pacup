import argparse
from . import backup
from . import check
from . import clear_cache
from . import generate_config
from . import install
from . import list_subcommand
from . import status
from .package_managers import valid_package_manager_names, package_managers

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

def setup_parser_backup(parser : argparse.ArgumentParser):
    parser.set_defaults(handler=backup.handler)
    #parser.add_argument("-l", "--package-list")

def setup_parser_check(parser):
    parser.set_defaults(handler=check.handler)
    add_package_managers_argument(parser)

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
