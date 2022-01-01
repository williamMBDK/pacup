from typing import Optional
from ..util.package import PackageFactory, Package
from ..util.output import PacupUserError

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
            if items[0] not in ConfigurationElement.valid_modifiers: raise PacupUserError("invalid modifier")
            self.modifier = items[0]
            if items[1] not in ConfigurationElement.valid_single_types: raise PacupUserError("invalid single type")
            self.type = items[1]
        elif len(items) == 3:
            if items[0] not in ConfigurationElement.valid_modifiers: raise PacupUserError("invalid modifier")
            self.modifier = items[0]
            if items[1] not in ConfigurationElement.valid_value_types: raise PacupUserError("invalid value type")
            self.type = items[1]
            self._set_value(items[2])
        else:
            raise PacupUserError("invalid length of line in config")
        self.has_been_initialized = True

    def _set_value(self, string : str):
        assert(self.type in ConfigurationElement.valid_value_types)
        if self.type == "tag": self.tag = string
        elif self.type == "pac": self.package = PackageFactory.create_package_from_string(string)

    def get_value(self):
        assert(self.has_been_initialized)
        if self.type == "tag": return self.tag
        elif self.type == "pac": return self.package
        else: raise Exception("element does not have a value")

    def has_value(self):
        assert(self.has_been_initialized)
        return ConfigurationElement.valid_value_types.count(self.type) == 1

class ConfigurationElementFactory:
    
    @staticmethod
    def create_configuration_element_from_string(input_string) -> ConfigurationElement:
        e = ConfigurationElement()
        e.init_with_string(input_string)
        return e
