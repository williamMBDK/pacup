from configuration.package import PackageFactory, TaggedPackage

class TaggedPackageList:
    def __init__(self):
        self.tagged_packages : list[TaggedPackage] = []
        self.has_been_initialized : bool = False

    def init_with_file_content(self, content : str):
        assert(not self.has_been_initialized)
        lines = content.split("\n")
        seen = set()
        for line in lines:
            if len(line.split()) == 0: continue
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

class TaggedPackageListFactory:
    @staticmethod
    def create_list_from_filename(filename) -> TaggedPackageList:
        with open(filename) as file:
            content = file.read()
            return TaggedPackageListFactory.create_list_from_content(content)

    @staticmethod
    def create_list_from_content(content) -> TaggedPackageList:
        paclist = TaggedPackageList()
        paclist.init_with_file_content(content)
        return paclist
