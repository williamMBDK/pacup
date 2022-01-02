# This package processes command line arguments using argparse.
# When argparse returns the args object a list of middleware functions
# has been provided by this package, and these middleware functions
# should all be called with args as argument. This was the args object
# will be prepared for whatever use it has later.

from .cli import create_parser
