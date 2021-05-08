#!/bin/python3

import sys
import color as color

filename = input()

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
    turn=True

    for line in sys.stdin.readlines():
        if line == "##########":
            turn = False
            continue
       
        # filter hashtags (comments) from line

        items = line.split()
        if len(items) == 0: continue

        configuration = Configuration(line)

        if turn:
            if not configuration.package in config1:
                config1[configuration.package] = []
            config1[configuration.package].append(configuration)
        else:
            if not configuration.package in config2:
                config2[configuration.package] = []
            config2[configuration.package].append(configuration)

    return config1, config2

def ask(question):
    while True:
        ans = input("{} [Y/n]: ".format(question))
        if ans == "y" or ans == " " or ans == "Y":
            return True
        elif ans == "n":
            return False
        else:
            print("Invalid input: {}".format(ans))

def resolve_duplicates(package_config, existing_package_configs):
    package_name = package_config.package
    assert(len(existing_package_configs) > 0)
    print("The following package configuration for {} already exist")
    for i, existing_package_config in enumerate(existing_package_configs):
        assert(existing_package_config.package == package_name)
        print("    {}. {}".format(i, existing_package_config))
    print("Do you wish to add it?")

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
            print("Package {} already exists in config ({})".format(package_name, filename))
            resolve_duplicates(package_config, config2[package_name])
        else:
            print("Package {} is not in config ({})".format(package_name, filename))
            if ask("Do you wish to add it?"):
                if not ask("Do you wish to include version?"):
                    package_config.version = None
                res.append(package_config)
            else:
                print("skipping")

    for package_name in config2:

        assert(package_name != None)
        assert(package_name.count(" ") == 0)
        assert(len(package_name) > 0)

        if package_name in config1: continue
        package_config = config1[package_name]

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
