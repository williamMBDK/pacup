import os, shutil
from .util.output import print_additional_info

def handler(args):
    path ="~/.cache/pacup"
    if args.verbosity > 0:
        print_additional_info("Deleing {}".format(path))
    try:
        shutil.rmtree(os.path.expanduser(path))
    except OSError:
        pass
