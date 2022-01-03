from .package_managers import PackageManager
from .util.io import PacupInstallError, lazy_confirm, print_error, print_needed_info, print_normal, print_success, print_additional_info, print_fill_width

def handler(args):
    for i,pm in enumerate(args.package_managers):
        if i > 0: print_normal()
        install_all_matches(args, pm)

def install_all_matches(args, pm : PackageManager):
    if args.verbosity >= 1: print_needed_info("INSTALLATION OF PACKAGES FOR {}".format(pm.name.upper()))
    matched_packages = pm.get_config().get_matching_packages(pm.get_list())
    for pac in matched_packages:
        if not pm.is_package_installed(pac):
            if args.verbosity >= 1 and not args.yes and not lazy_confirm("Do you wish to install {} using {}?".format(pac, pm.name)): continue
            if args.verbosity >= 1:
                print_needed_info("Beginning installation of {} using {}".format(pac, pm.name))
            if args.verbosity >= 1: print_fill_width('=')
            success = True
            error=None
            if not args.test:
                try:
                    pm.install_package(pac)
                except PacupInstallError as e:
                    error = e
                    success = False
            if args.verbosity >= 1: print_fill_width('=')
            if args.verbosity >= 1:
                if success: print_success("Installed {} using {}".format(pac, pm.name))
                else: print_error(error)
        else:
            if args.verbosity >= 1: print_additional_info("Package {} is installed".format(pac))
