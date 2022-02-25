from ..util.package import Package
from .configuration_element import ConfigurationElementFactory, ConfigurationElement
from .tagged_package_list import TaggedPackageList
from ..util.io import PacupUserError
from .util import remove_comments

class Configuration:
    def __init__(self):
        self.configuration_elements : list[ConfigurationElement] = []
        self.has_been_initialized : bool = False

    def init_with_file_content(self, content : str):
        lines = content.split("\n")
        seen = set()
        for line in lines:
            line = remove_comments(line)
            if len(line.split()) == 0: continue
            element = ConfigurationElementFactory.create_configuration_element_from_string(line)
            key = (
                element.modifier,
                element.type,
                str(element.get_value()) if element.has_value() else ""
            )
            if key in seen:
                raise PacupUserError("file content contains duplicate rule")
            seen.add(key)
            self.configuration_elements.append(element)

    def get_matching_packages(self, package_list : TaggedPackageList) -> list[Package]:
        packages : set[Package] = set()
        tags = package_list.get_tag_map()
        def remove_package(to_remove : Package):
            if to_remove in packages: packages.remove(to_remove)
        for element in self.configuration_elements:
            if element.modifier == "+":
                if element.type == "pac":
                    if not package_list.contains(element.package.copy()): # type: ignore
                        raise PacupUserError("{} not in tagged package list".format(element.package))
                    packages.add(element.package.copy()) # type: ignore
                elif element.type == "tag":
                    if element.tag not in tags: continue
                    packages.update(tags[str(element.tag)])
                elif element.type == "all": packages.update(set(tagged_package.copy_as_package() for tagged_package in package_list.tagged_packages))
            else:
                if element.type == "pac":
                    if not package_list.contains(element.package.copy()): # type: ignore
                        raise PacupUserError("{} not in tagged package list".format(element.package))
                    remove_package(element.package.copy()) # type: ignore
                elif element.type == "tag":
                    if element.tag not in tags: continue
                    for package in tags[str(element.tag)]: remove_package(package)
                elif element.type == "all": packages = set()
        names = set()
        for package in packages:
            if package.name in names:
                raise PacupUserError("A package was specified more than once with name {}".format(package.name))
            names.add(package.name)
        return sorted(list(packages))

class ConfigurationFactory:

    @staticmethod
    def create_configuration_from_filename(filename) -> Configuration:
        content = None
        try:
            with open(filename) as file:
                content = file.read()
        except FileNotFoundError: raise PacupUserError("config path does not exist")
        except IsADirectoryError: raise PacupUserError("config path is a directory")
        assert(content != None)
        return ConfigurationFactory.create_configuration_from_content(content)

    @staticmethod
    def create_configuration_from_content(content) -> Configuration:
        config = Configuration()
        config.init_with_file_content(content)
        return config
