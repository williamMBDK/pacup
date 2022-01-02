from ..package_managers import valid_package_manager_names, get_package_managers, PackageManager
from ..util.output import print_warning
from .middleware import add_middleware

def add_package_managers_argument(parser):
    # 'all' is a hack to fix this bug: https://bugs.python.org/issue41047
    parser.add_argument(
        "package_managers",
        nargs="*",
        choices=valid_package_manager_names + ["all"], 
        help="package manager: {}".format(", ".join(valid_package_manager_names)),
        default="all",
        metavar="package-manager",
    )

# depends on: args.verbosity
def add_package_managers_middleware(parser):
    def f(args):
        assert(hasattr(args, "package_managers"))
        values = args.package_managers
        if values == "all" or "all" in values:
            values = valid_package_manager_names
        values = set(values)
        args.package_managers = list(filter(lambda pm: pm.name in values, get_package_managers()))
        new_packages_managers = []
        for pm in args.package_managers:
            pm : PackageManager = pm
            if not pm.is_installed():
                if args.verbosity >= 2:
                    print_warning(
                        "ignoring package-manager {} as it is not installed"
                        .format(pm.name)
                    )
                continue
            new_packages_managers.append(pm)
        args.package_managers = new_packages_managers
    add_middleware(parser, f)
