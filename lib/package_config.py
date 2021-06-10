__all__ = ["PackageListFactory", "ConfigurationFactory"]

from typing import Optional
import copy

class Package:
    def __init__(self):
        self.name : str = ""
        self.version : Optional[str] = None
        self.has_been_initialized : bool = False
        
    def init_with_string(self, input_string):
        assert(not self.has_been_initialized)
        items = input_string.split()
        if len(items) != 1:
            raise ValueError("invalid input_string")
        item = items[0]
        if item.count("@"):
            self.name = item[:item.index("@")]
            self.version = item[item.index("@")+1:]
        else:
            self.name = item
        self.has_been_initialized = True

    def init_with_values(self, name, version):
        self.name = name
        self.version = version
        self.has_been_initialized = True

    def __str__(self):
        assert(self.has_been_initialized)
        if self.version:
            return "{}@{}".format(self.name, self.version)
        else:
            return self.name

class TaggedPackage(Package):
    def __init__(self):
        super().__init__()
        self.tags : list[str] = []
        
    def init_with_string(self, input_string):
        assert(not self.has_been_initialized)
        items = input_string.split()
        if len(items) == 0:
            raise ValueError("invalid input_string")
        super().init_with_string(items[0])
        self.tags = items[1:]

    def __str__(self):
        assert(self.has_been_initialized)
        return "{} ({})".format(super().__str__(), " ".join(self.tags))

class PackageFactory:
    
    @staticmethod
    def create_package_from_string(input_string) -> Package:
        pac = Package()
        pac.init_with_string(input_string)
        return pac

    @staticmethod
    def create_package_from_values(name : str, version : str) -> Package:
        pac = Package()
        pac.init_with_values(name, version)
        return pac

    @staticmethod
    def create_tagged_package_from_string(input_string) -> TaggedPackage:
        pac = TaggedPackage()
        pac.init_with_string(input_string)
        return pac

class PackageList:
    def __init__(self):
        self.tagged_packages : list[TaggedPackage] = []
        self.has_been_initialized : bool = False

    def init_with_file_content(self, content : str):
        assert(not self.has_been_initialized)
        lines = content.split()
        seen = set()
        for line in lines:
            if line == "": continue
            pac = PackageFactory.create_tagged_package_from_string(line)
            key = (pac.name, pac.version)
            if key in seen:
                raise ValueError("content contains duplicate package@version")
            seen.add(key)
            self.tagged_packages.append(pac)
        self.has_been_initialized = True

    def __str__(self):
        assert(self.has_been_initialized)
        return "\n".join(map(str, self.tagged_packages))

class PackageListFactory:
    @staticmethod
    def create_list_from_filename(filename) -> PackageList:
        with open(filename) as file:
            content = file.read()
            paclist = PackageList()
            paclist.init_with_file_content(content)
            return paclist

class ConfigurationElement:

    valid_modifiers = ["+", "-"]
    valid_single_types = ["all"]
    valid_value_types = ["pac", "tag"]

    def __init__(self):
        self.modifier : str = ""
        self.type : str = ""
        # value
        self.tag : Optional[str] = None
        self.package: Optional[Package] = None

        self.has_been_initialized : bool = False

    def init_with_string(self, input_string):
        assert(not self.has_been_initialized)
        items = input_string.split()
        if len(items) == 2:
            if items[0] not in ConfigurationElement.valid_modifiers: raise ValueError("invalid modifier")
            self.modifier = items[0]
            if items[1] not in ConfigurationElement.valid_single_types: raise ValueError("invalid single type")
            self.type = items[1]
        elif len(items) == 3:
            if items[0] not in ConfigurationElement.valid_modifiers: raise ValueError("invalid modifier")
            self.modifier = items[0]
            if items[1] not in ConfigurationElement.valid_value_types: raise ValueError("invalid value type")
            self.type = items[1]
            self._set_value(items[2])
        else:
            raise ValueError("invalid input_string length")
        self.has_been_initialized = True

    def _set_value(self, string : str):
        assert(self.type in ConfigurationElement.valid_value_types)
        if self.type == "tag": self.tag = string
        elif self.type == "pac": self.package = PackageFactory.create_package_from_string(string)

    def get_value(self):
        assert(self.has_been_initialized)
        if self.type == "tag": return self.tag
        elif self.type == "pac": return self.package

class ConfigurationElementFactory:
    
    @staticmethod
    def create_configuration_element_from_string(input_string) -> ConfigurationElement:
        e = ConfigurationElement()
        e.init_with_string(input_string)
        return e

class Configuration:
    def __init__(self):
        self.configuration_elements : list[ConfigurationElement] = []
        self.has_been_initialized : bool = False

    def init_with_file_content(self, content : str):
        lines = content.split()
        seen = set()
        for line in lines:
            if line == "": continue
            element = ConfigurationElementFactory.create_configuration_element_from_string(line)
            key = (element.modifier, element.type, str(element.get_value()))
            if key in seen:
                raise ValueError("content contains duplicate rule")
            seen.add(key)
            self.configuration_elements.append(element)

    def get_matching_packages(self, package_list : PackageList) -> list[Package]:
        packages = set()
        tags = {}
        tags["all"] = set((tagged_package.name, tagged_package.version) for tagged_package in package_list.tagged_packages)
        for tagged_package in package_list.tagged_packages:
            for tag in tagged_package.tags:
                if tag not in tags: tags[tag] = set()
                tags[tag].add((tagged_package.name, tagged_package.version))
        for element in self.configuration_elements:
            if element.modifier == "+":
                if element.type == "pac": packages.add((element.package.name, element.package.version))
                elif element.type == "tag": packages += tags[element.tag]
        flagged_names = set()
        for element in self.configuration_elements:
            if element.modifier == "-":
                if element.type == "pac":
                    to_remove = (element.package.name, element.package.version)
                    if to_remove[1] == None: flagged_names.add(to_remove[0])
                    if to_remove in packages: packages.remove(to_remove)
                elif element.type == "tag":
                    for to_remove in tags[element.tag]:
                        to_remove = (element.package.name, element.package.version)
                        if to_remove[1] == None: flagged_names.add(to_remove[0])
                        if to_remove in packages: packages.remove(to_remove)
        result : list[Package] = []
        for pac in packages:
            if pac[0] not in flagged_names:
                result.append(PackageFactory.create_package_from_values(pac[0], pac[1]))
        names = set()
        for package in result:
            if package.name in names:
                raise ValueError("invalid package list")
            names.add(package.name)
        return result

class ConfigurationFactory:
    @staticmethod
    def create_configuration_from_filename(filename) -> Configuration:
        with open(filename) as file:
            content = file.read()
            config = Configuration()
            config.init_with_file_content(content)
            return config
