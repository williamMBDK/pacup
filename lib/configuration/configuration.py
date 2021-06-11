from configuration.package import PackageFactory, Package
from configuration.configuration_element import ConfigurationElementFactory, ConfigurationElement
from configuration.tagged_package_list import TaggedPackageList

class Configuration:
    def __init__(self):
        self.configuration_elements : list[ConfigurationElement] = []
        self.has_been_initialized : bool = False

    def init_with_file_content(self, content : str):
        lines = content.split("\n")
        seen = set()
        for line in lines:
            if len(line.split()) == 0: continue
            element = ConfigurationElementFactory.create_configuration_element_from_string(line)
            key = (
                element.modifier,
                element.type,
                str(element.get_value()) if element.has_value() else ""
            )
            if key in seen:
                raise ValueError("content contains duplicate rule")
            seen.add(key)
            self.configuration_elements.append(element)

    def get_matching_packages(self, package_list : TaggedPackageList): #  -> list[Package]:
        packages = set()
        # getting tags
        tags = {}
        for tagged_package in package_list.tagged_packages:
            for tag in tagged_package.tags:
                if tag not in tags: tags[tag] = set()
                tags[tag].add((tagged_package.name, tagged_package.version))
        for element in self.configuration_elements:
            if element.modifier == "+":
                if element.type == "pac": packages.add((element.package.name, element.package.version))
                elif element.type == "tag": packages.update(tags[element.tag])
                elif element.type == "all": packages.update(set((tagged_package.name, tagged_package.version) for tagged_package in package_list.tagged_packages))
        flagged_names = set()
        for element in self.configuration_elements:
            if element.modifier == "-":
                if element.type == "pac":
                    to_remove = (element.package.name, element.package.version)
                    if to_remove[1] == None: flagged_names.add(to_remove[0])
                    if to_remove in packages: packages.remove(to_remove)
                elif element.type == "tag":
                    for to_remove in tags[element.tag]:
                        if to_remove[1] == None: flagged_names.add(to_remove[0])
                        if to_remove in packages: packages.remove(to_remove)
                elif element.type == "all":
                    return []
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
            return ConfigurationFactory.create_configuration_from_content(content)

    @staticmethod
    def create_configuration_from_content(content) -> Configuration:
        config = Configuration()
        config.init_with_file_content(content)
        return config

