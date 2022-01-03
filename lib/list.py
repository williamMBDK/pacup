from .util.io import print_normal, print_success
from .package_managers import PackageManager

def handler(args):
    for pm in args.package_managers:
        pm : PackageManager = pm
        if args.perform_count:
            count = len(pm.get_installed_packages())
            if args.verbosity >= 1:
                print_success(
                    "Number of explicitely installed packages for {} is {}".format(
                        pm.name.upper(), count
                    )
                )
            else:
                print_normal(count)
        else:
            if args.verbosity >= 1: print_success("Explicitely installed packages for {}".format(pm.name.upper()))
            for pac in pm.get_installed_packages():
                if args.with_version: print_normal(pac)
                else: print_normal(pac.get_name())
