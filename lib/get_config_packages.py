#!/usr/bin/python3

import sys
from configuration.configuration import ConfigurationFactory
from configuration.tagged_package_list import TaggedPackageListFactory, TaggedPackageList
from utility.color import TermColors

if len(sys.argv) != 3:
    print("{}ERROR: expected 2 arguments (path-to-config path-to-package-list){}".format(TermColors.RED, TermColors.NOCOLOR))
    exit(1)

configname = sys.argv[1]
listname = sys.argv[2]

config = None
taggedlist = TaggedPackageList()

try:
    config = ConfigurationFactory.create_configuration_from_filename(configname)
except FileNotFoundError:
    print("{}ERROR: config path does not exist{}".format(TermColors.RED, TermColors.NOCOLOR))
    exit(1)
except IsADirectoryError:
    print("{}ERROR: config path is a directory{}".format(TermColors.RED, TermColors.NOCOLOR))
    exit(1)
except ValueError:
    print("{}ERROR: invalid syntax in config{}".format(TermColors.RED, TermColors.NOCOLOR))
    exit(1)

try:
    taggedlist = TaggedPackageListFactory.create_list_from_filename(listname)
except FileNotFoundError:
    print("{}ERROR: package list path does not exist{}".format(TermColors.RED, TermColors.NOCOLOR))
    exit(1)
except IsADirectoryError:
    print("{}ERROR: package list path is a directory{}".format(TermColors.RED, TermColors.NOCOLOR))
    exit(1)
except ValueError:
    print("{}ERROR: invalid syntax in package list{}".format(TermColors.RED, TermColors.NOCOLOR))
    exit(1)

matched_packages = []
try:
    matched_packages = config.get_matching_packages(taggedlist)
except ValueError:
    print("{}ERROR: incomplete config{}".format(TermColors.RED, TermColors.NOCOLOR))
    exit(1)

print("{}MATCHED PACKAGES{}".format(TermColors.GREEN, TermColors.NOCOLOR))
for package in matched_packages:
    print(package)

