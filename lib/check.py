from .package_managers import PackageManager
from .util.io import print_normal, print_success

def handler(args):
    for pm in args.package_managers:
        pm : PackageManager = pm
        if args.verbosity >= 1: print_success("Matched packages for {}".format(pm.name.upper()))
        matched_packages = pm.get_config().get_matching_packages(pm.get_list())
        for pac in matched_packages: print_normal(pac)
