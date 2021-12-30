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
            return self.get_name()

    def get_name(self):
        return self.name
    
    def copy(self):
        return PackageFactory.create_package_from_values(self.name, self.version)

    def  __eq__(self, other):
        return self.name == other.name and self.version == other.version

    def __hash__(self):
        return hash(self.name) * hash(self.version) # not sure if this is good?

    def __lt__(self, other):
        if self.name == other.name:
            if self.version == None: return other.version != None
            elif other.version == None: return False
            else: return self.version < other.version
        return self.name < other.name
    
    def without_version(self):
        return PackageFactory.create_package_from_values(self.name, None)

class PackageFactory:
    
    @staticmethod
    def create_package_from_string(input_string) -> Package:
        pac = Package()
        pac.init_with_string(input_string)
        return pac

    @staticmethod
    def create_package_from_values(name : str, version : Optional[str]) -> Package:
        pac = Package()
        pac.init_with_values(name, version)
        return pac
