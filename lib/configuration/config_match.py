import sys
from .configuration import ConfigurationFactory
from .tagged_package_list import TaggedPackageListFactory, TaggedPackageList

CONFIG=sys.argv[1]
PACLIST=sys.argv[2]

config = None
taggedlist = TaggedPackageList()

try:
    config = ConfigurationFactory.create_configuration_from_filename(CONFIG)
except FileNotFoundError:
    print("config path does not exist")
    exit(1)
except IsADirectoryError:
    print("config path is a directory")
    exit(1)
except ValueError:
    print("invalid syntax in config")
    exit(1)

try:
    taggedlist = TaggedPackageListFactory.create_list_from_filename(PACLIST)
except FileNotFoundError:
    print("package list path does not exist")
    exit(1)
except IsADirectoryError:
    print("package list path is a directory")
    exit(1)
except ValueError:
    print("invalid syntax in package list")
    exit(1)

matched_packages = []
try:
    matched_packages = config.get_matching_packages(taggedlist)
except ValueError as e:
    print("incomplete config: ", e)
    exit(1)

for package in matched_packages:
    if package.version: print("{}@{}".format(package.name, package.version))
    else: print(package.name)
