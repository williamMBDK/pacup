from typing import Optional

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
        assert(not self.has_been_initialized)
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
