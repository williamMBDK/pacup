from .tagged_package import TaggedPackageFactory, TaggedPackage
from ..util.package import PackageFactory, Package
from ..util.io import PacupUserError
from .util import remove_comments

class TaggedPackageList:
    def __init__(self):
        self.tagged_packages : list[TaggedPackage] = []
        self.has_been_initialized : bool = False

    def init_with_file_content(self, content : str):
        assert(not self.has_been_initialized)
        lines = content.split("\n")
        seen = set()
        for line in lines:
            line = remove_comments(line)
            if len(line.split()) == 0: continue
            pac = TaggedPackageFactory.create_tagged_package_from_string(line)
            key = (pac.name, pac.version)
            if key in seen:
                raise PacupUserError("list contains duplicate package@version")
            seen.add(key)
            self.tagged_packages.append(pac)
        self.has_been_initialized = True

    def __str__(self):
        assert(self.has_been_initialized)
        self.tagged_packages.sort()
        return "\n".join(map(str, self.tagged_packages))
    
    def get_tag_map(self) -> dict[str, set[Package]]:
        assert(self.has_been_initialized)
        tags = {}
        for tagged_package in self.tagged_packages:
            for tag in tagged_package.tags:
                if tag not in tags: tags[tag] = set()
                tags[tag].add(PackageFactory.create_package_from_values(tagged_package.name, tagged_package.version))
        return tags
    
    def contains(self, package : Package):
        # TODO can be optimized
        return package in self.tagged_packages
    
    def write_to_file(self, filename : str):
        with open(filename, 'w') as file:
            file.write(str(self))

    def append_to_file(self, filename : str):
        with open(filename, 'a') as file:
            file.write("\n" + str(self))

    def append(self, tagged_package : TaggedPackage):
        # todo?: this can be done faster
        for package in self.tagged_packages:
            if package.name == tagged_package.name and package.version == tagged_package.version:
                raise PacupUserError("list will contain duplicate package@version after appending {}".format(tagged_package))
        self.tagged_packages.append(tagged_package)

    def append_str(self, string : str):
        self.append(TaggedPackageFactory.create_tagged_package_from_string(string))

class TaggedPackageListFactory:

    @staticmethod
    def create_list_from_filename(filename) -> TaggedPackageList:
        content = None
        try:
            with open(filename) as file:
                content = file.read()
        except FileNotFoundError:
            raise PacupUserError(
                "package list path does not exist: {}"
                .format(filename)
            )
        except IsADirectoryError:
            raise PacupUserError(
                "package list path is a directory: {}"
                .format(filename)
            )
        assert(content != None)
        return TaggedPackageListFactory.create_list_from_content(content)

    @staticmethod
    def create_list_from_content(content) -> TaggedPackageList:
        paclist = TaggedPackageList()
        paclist.init_with_file_content(content)
        return paclist

    @staticmethod
    def create_empty_list() -> TaggedPackageList:
        return TaggedPackageListFactory.create_list_from_content("")
