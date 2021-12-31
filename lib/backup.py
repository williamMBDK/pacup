from .package_managers import package_managers
from .util.package import PackageFactory

def handler(args):
    print("backup handler")
    #print(args.package_managers)
    #print(package_managers[3].is_installed())
    #print(package_managers[3].get_installed_packages())
    #print(package_managers[3].install_package(PackageFactory.create_package_from_values("xsnow", None)))
    #print(package_managers[3].is_package_installed(PackageFactory.create_package_from_values("zip", None)))
