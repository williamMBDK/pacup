#!/bin/python3

import sys
import color as color
from typing import Optional

pmoutputfilename = sys.argv[1]
configfilename = sys.argv[2]

print(pmoutputfilename, configfilename)

class Configuration:
    def __init__(self, input_string):
        items = input_string.split()
        assert(len(items) > 0)
        self.package = ""
        self.version = None
        if items[0].count("@"):
            self.package = items[0][:items[0].index("@")]
            self.version = items[0][items[0].index("@")+1:]
        else:
            self.package = items[0]
        self.tags = items[1:]

    def __str__(self):
        if self.version:
            return self.package + "@" + self.version + " " + " ".join(self.tags)
        else:
            return self.package + " " + " ".join(self.tags)

def build():
    config1 = {}
    config2 = {}

    # todo: filter hashtags (comments) from line

    with open(pmoutputfilename) as fp:
        for line in fp.readlines():
            items = line.split()
            if len(items) == 0: continue
            configuration = Configuration(line)
            if not configuration.package in config1:
                config1[configuration.package] = []
            config1[configuration.package].append(configuration)
    with open(configfilename) as fp:
        for line in fp.readlines():
            items = line.split()
            if len(items) == 0: continue
            configuration = Configuration(line)
            if not configuration.package in config2:
                config2[configuration.package] = []
            config2[configuration.package].append(configuration)
        
    return config1, config2

def ask(question, preferyes=True):
    while True:
        ans = input("{} [Y/n]: ".format(question)) if preferyes else input("{} [y/N]: ".format(question))
        if ans == "y" or ans == "Y" or (preferyes and ans == ""):
            return True
        elif ans == "n" or ans == "N" or ((not preferyes) and ans == ""):
            return False
        else:
            print("Invalid input: {}".format(ans))

def resolve_duplicates(package_config, existing_package_configs):
    package_name = package_config.package
    assert(len(existing_package_configs) > 0)

    def exist():
        for existing_package_config in existing_package_configs:
            assert(existing_package_config.package == package_name)
            if existing_package_config.version == package_config.version:
                return True
        return False

    if exist():
        return existing_package_configs

    print("Package {} already exists in config ({}) as the following configurations".format(package_name, configfilename))
    for i, existing_package_config in enumerate(existing_package_configs):
        print("    {}. {}".format(i+1, existing_package_config))

    all_package_configs = []

    if ask("Do you wish to add it again?"):
        if not ask("Do you wish to include version?", False):
            package_config.version = None
        if exist():
            print("Requirement already satisfied")
            return existing_package_configs
        else:
            print("Adding to config: {}", package_config)
            all_package_configs = existing_package_configs + [package_config]
    else:
        return existing_package_configs
    resulting_package_configs = []
    if ask("Do you wish to review the new package configs for {}?".format(package_name)):
        print("Config now contains the following package configuration for {}".format(package_name))
        for i, new_package_config in enumerate(all_package_configs):
            print("    {}. {}".format(i+1, new_package_config))
        def parse(s) -> Optional[list[int]]:
            arr = s.split()
            result = []
            for s in arr:
                try:
                    result.append(int(s) - 1)
                except:
                    return None
            for num in result:
                if num < 0 or num >= len(all_package_configs):
                    return None
            return result
        while True:
            should_be_removed = input("Enter which should be removed [space seperated 1-{}]: ".format(len(all_package_configs)))
            parsed = parse(should_be_removed)
            if parsed == None:
                print("Invalid input: {}".format(should_be_removed))
                continue
            for i, package_config in enumerate(all_package_configs):
                if parsed and not i in parsed: # pyright do not like it if we dont check that parsed "is"
                    resulting_package_configs.append(package_config)
                else:
                    print("Removing from config: {}".format(package_config))
            break
    else:
        resulting_package_configs = all_package_configs
    return resulting_package_configs

def analyze(config1, config2):
    res=[]

    for package_name in config1:

        assert(package_name != None)
        assert(package_name.count(" ") == 0)
        assert(len(package_name) > 0)
        assert(len(config1[package_name]) == 1)

        package_config = config1[package_name][0]

        assert(package_config.version != None)
        assert(package_config.package != None)
        assert(package_config.package != "")
        assert(package_config.tags == [])

        if package_name in config2:
            res += resolve_duplicates(package_config, config2[package_name])
        else:
            print("Package {} is not in config ({})".format(package_name, configfilename))
            if ask("Do you wish to add it?"):
                if not ask("Do you wish to include version?", False):
                    package_config.version = None
                print("Adding to config: {}".format(package_config))
                res.append(package_config)
            else:
                print("skipping")

    for package_name in config2:

        assert(package_name != None)
        assert(package_name.count(" ") == 0)
        assert(len(package_name) > 0)

        if package_name in config1: continue
        package_config = config2[package_name]

        assert(package_config.package_name != None)
        assert(package_config.package_name != "")
        
        res.append(package_config)

    return res

def output(config):
    for package_config in config:
        print(package_config)

config1, config2 = build()
res = analyze(config1, config2)
output(res)

exit(0)
