#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

from .middleware import create_parser
from .util.io import PacupUserError, PacupUnknownError, print_error
import signal, sys

def siginthandler(sig, frame):
    sys.exit(0)

def main():

    signal.signal(signal.SIGINT, siginthandler)

    parser = create_parser()

    # bash autocompletion
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    # get cli arguments
    args = parser.parse_args()

    # run handler for a given subcommand (see https://docs.python.org/3/library/argparse.html#the-add-argument-method)
    if hasattr(args, "handler"):
        try:
            for f in args.middleware: # type: ignore
                f(args)
            args.handler(args)
        except PacupUserError as e:
            print_error(e)
            sys.exit(1)
        except PacupUnknownError as e:
            print_error(e)
            sys.exit(2)
    else:
        parser.print_help()

    sys.exit(0)
