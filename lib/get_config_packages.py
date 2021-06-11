import sys
from configuration.configuration import ConfigurationFactory
from configuration.tagged_package_list import TaggedPackageListFactory

if len(sys.argv) != 3:
    exit(1)
configname = sys.argv[1]
listname = sys.argv[2]

config = ConfigurationFactory.create_configuration_from_filename(configname)
taggedlist = TaggedPackageListFactory.create_list_from_filename(listname)

matched_packages = config.get_matching_packages(taggedlist)

for package in matched_packages:
    print(package)
