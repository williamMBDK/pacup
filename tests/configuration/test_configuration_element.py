import unittest
from configuration.configuration_element import ConfigurationElement
from configuration.package import Package

class TestConfigurationElement(unittest.TestCase):
    def setUp(self):
        self.element = ConfigurationElement()

    def test_init_with_string_single_type(self):
        tests = [
            ("+ all", "+", "all"),
            ("- all", "-", "all"),
        ]
        for (string, mod, typ) in tests:
            self.element = ConfigurationElement()
            self.element.init_with_string(string)
            self.assertEqual("all", self.element.type)
            self.assertEqual(mod, self.element.modifier)
            self.assertEqual(typ, self.element.type)

    def test_init_with_string_invalid_modifier(self):
        def test():
            self.element.init_with_string("  s all")
        self.assertRaises(ValueError, test) 

    def test_init_with_string_single_type_fail(self):
        def test():
            self.element.init_with_string("+ tag")
        self.assertRaises(ValueError, test) 

    def test_init_with_value_type_fail(self):
        def test():
            self.element.init_with_string("+ all sdf")
        self.assertRaises(ValueError, test) 

    def test_init_with_string_tag(self):
        tests = [
            ("+ tag a", "+", "a"),
            ("- tag a", "-", "a"),
            ("+ tag abc", "+", "abc"),

        ]
        for (string, mod, tagvalue) in tests:
            self.element = ConfigurationElement()
            self.element.init_with_string(string)
            self.assertEqual("tag", self.element.type)
            self.assertEqual(mod, self.element.modifier)
            self.assertEqual(tagvalue, self.element.tag)

    def test_init_with_string_pac(self):
        tests = [
            ("+ pac a", "+", "a", None),
            ("- pac a@1", "-", "a", "1"),
        ]
        for (string, mod, name, version) in tests:
            self.element = ConfigurationElement()
            self.element.init_with_string(string)
            self.assertEqual("pac", self.element.type)
            self.assertEqual(mod, self.element.modifier)
            self.assertEqual(name, self.element.package.name)
            self.assertEqual(version, self.element.package.version)

    def test_get_value_pac(self):
        self.element.init_with_string("+ pac a")
        self.assertIsInstance(self.element.get_value(), Package)

    def test_get_value_tag(self):
        self.element.init_with_string("+ tag a")
        self.assertEqual(self.element.get_value(), "a")

    def test_get_value_fail(self):
        self.element.init_with_string("+ all")
        self.assertRaises(Exception, self.element.get_value)
