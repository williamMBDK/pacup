#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

from . import cli

def main():
    parser = cli.create_parser()

    # bash autocompletion
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    # get cli arguments
    args = parser.parse_args()

    # run handler for a given subcommand (see https://docs.python.org/3/library/argparse.html#the-add-argument-method)
    args.handler(args)
