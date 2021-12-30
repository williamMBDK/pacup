from ..util.package import Package

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

    def init_with_values(self, name, version, tags):
        super().init_with_values(name, version)
        self.tags = tags

    def __str__(self):
        assert(self.has_been_initialized)
        return "{} {}".format(super().__str__(), " ".join(self.tags))

    def copy(self):
        return TaggedPackageFactory.create_tagged_package_from_values(self.name, self.version, self.tags.copy())

    def copy_as_package(self):
        return super().copy()

class TaggedPackageFactory:
    
    @staticmethod
    def create_tagged_package_from_string(input_string) -> TaggedPackage:
        pac = TaggedPackage()
        pac.init_with_string(input_string)
        return pac

    @staticmethod
    def create_tagged_package_from_values(name, version, tags) -> TaggedPackage:
        pac = TaggedPackage()
        pac.init_with_values(name, version, tags)
        return pac
