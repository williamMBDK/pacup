from .package_managers import PackageManager

def handler(args):
    print("check handler")
    for package_manager in args.package_managers:
        package_manager : PackageManager = package_manager # type checker
