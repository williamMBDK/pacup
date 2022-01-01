from .package_managers import PackageManager
from .configuration import ConfigurationFactory, TaggedPackageListFactory
from .util.output import print_normal

def handler(args):
    for pm in args.package_managers:
        pm : PackageManager = pm # type checker
        configuration = ConfigurationFactory.create_configuration_from_config(pm.name)
        tagged_list = TaggedPackageListFactory.create_list_from_config(pm.name)
        matched_packages = configuration.get_matching_packages(tagged_list)
        for package in matched_packages: print_normal(package)
