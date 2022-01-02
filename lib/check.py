from .util.output import print_normal, print_success

def handler(args):
    for pm in args.package_managers:
        print_success("Matched packages for {}".format(pm.name.upper()))
        matched_packages = pm.config.get_matching_packages(pm.list)
        for package in matched_packages: print_normal(package)
