#!/usr/bin/python3

import sys
from configuration.configuration import ConfigurationFactory
from configuration.tagged_package_list import TaggedPackageListFactory, TaggedPackageList
from utility.color import TermColors
from getopt import getopt

opts, _ = getopt(sys.argv[1:], "qc:l:", ["quiet", "configuration=", "package-list="])

QUIET=False
CONFIG=None
PACLIST=None

for o, a in opts:
    if o in ("-q", "--quiet"): QUIET = True
    elif o in ("-c", "--configuration"): CONFIG = a
    elif o in ("-l", "--package-list"): PACLIST = a

config = None
taggedlist = TaggedPackageList()

try:
    config = ConfigurationFactory.create_configuration_from_filename(CONFIG)
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
    taggedlist = TaggedPackageListFactory.create_list_from_filename(PACLIST)
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
except ValueError as e:
    print("{}ERROR: incomplete config{}".format(TermColors.RED, TermColors.NOCOLOR))
    print("Interpreter output:")
    print("  ", e)
    exit(1)

if not QUIET: print("{}MATCHED PACKAGES{}".format(TermColors.GREEN, TermColors.NOCOLOR))
for package in matched_packages:
    if package.version: print(package.name, package.version)
    else: print(package.name)

