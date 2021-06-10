from lib import package_config
import unittest

class TestPackage(unittest.TestCase):

    def setUp(self):
        self.package = package_config.Package()

    def test_init(self):
        self.assertEqual(self.package.name, "")
        self.assertEqual(self.package.version, None)
        self.assertEqual(self.package.has_been_initialized, False)

    def assert_values(self, name, version):
        self.assertEqual(name, self.package.name)
        self.assertEqual(version, self.package.version)

    def test_str_not_init(self):
        err = False
        try:
            self.package.__str__()
        except AssertionError:
            err = True
        self.assertTrue(err)

    def test_init_with_values(self):
        self.package.init_with_values("a","1")
        self.assert_values("a", "1")

    def test_init_twice_with_values(self):
        self.package.init_with_values("a","1")
        err = False
        try:
            self.package.init_with_values("a","1")
        except AssertionError:
            err = True
        self.assertTrue(err)

    def test_init_with_string(self):
        tests = [
            ('a', ('a', None)),
            ('   a    ', ('a', None)),
            ('abc', ('abc', None)),
            ('a@b', ('a', 'b')),
            ('   a@b   ', ('a', 'b')),
            ('package@1.2.3.4', ('package', '1.2.3.4')),
            ('package@1.2.@3.4', ('package', '1.2.@3.4')),
        ]
        for (string, (exname, exversion)) in tests:
            self.package = package_config.Package()
            self.package.init_with_string(string)
            self.assert_values(exname, exversion)

    def test_init_with_invalid_string(self):
        tests = [
                "",
                "         ",
                "sdfsf sdfsd",
                "a a a a",
                "      a     a    a    a  "
        ]
        for string in tests:
            self.package = package_config.Package()
            err = False
            try:
                self.package.init_with_string(string)
            except ValueError:
                err = True
            self.assertTrue(err)

    def test_init_twice_with_string(self):
        self.package.init_with_string("sdfsdf")
        err = False
        try:
            self.package.init_with_string("sdf")
        except AssertionError:
            err = True
        self.assertTrue(err)

    def test_init_different_twice_with_string(self):
        self.package.init_with_string("sdfsdf")
        err = False
        try:
            self.package.init_with_values("sdf", "234")
        except AssertionError:
            err = True
        self.assertTrue(err)

class TestTaggedPackage(unittest.TestCase):
    def setUp(self):
        self.package = package_config.TaggedPackage()

    def test_base_init_with_string(self):
        self.package.init_with_string("a@1 a b c") 
        self.assertEqual("a", self.package.name)
        self.assertEqual("1", self.package.version)

    def test_init_with_string(self):
        tests = [
            ("a@1 a b c", ['a','b','c']),
            ("   a@1    a    b    c  ", ['a','b','c']),
            ("   a@1  ", []),
            ("a@1", [])
        ]
        for (string, expected) in tests:
            self.package = package_config.TaggedPackage()
            self.package.init_with_string(string) 
            self.assertEqual(expected, self.package.tags)

class TestTaggedPackageList(unittest.TestCase):
    def setUp(self):
        self.package_list = package_config.TaggedPackageList()

    def test_init_with_file_content(self):
        self.package_list.init_with_file_content(
            """
            a@1 e f g a


            b@2 
            c@3 tag

            """
        )
        self.assertEqual(3, len(self.package_list.tagged_packages))
        self.assertEqual("a", self.package_list.tagged_packages[0].name)
        self.assertEqual("b", self.package_list.tagged_packages[1].name)
        self.assertEqual("c", self.package_list.tagged_packages[2].name)
    
    def test_duplicate_init_with_file_content(self):
        err = False
        try:
            self.package_list.init_with_file_content(
                """
                a@1 e f g a
                a@1 sdf sf 
                """
            )
        except ValueError:
            err = True
        self.assertTrue(err)


class TestConfigurationElement(unittest.TestCase):
    def setUp(self):
        self.element = package_config.ConfigurationElement()

    def test_init_with_string_single_type(self):
        tests = [
            ("+ all", "+", "all"),
            ("- all", "-", "all"),
        ]
        for (string, mod, typ) in tests:
            self.element = package_config.ConfigurationElement()
            self.element.init_with_string(string)
            self.assertEqual("all", self.element.type)
            self.assertEqual(mod, self.element.modifier)
            self.assertEqual(typ, self.element.type)

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
            self.element = package_config.ConfigurationElement()
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
            self.element = package_config.ConfigurationElement()
            self.element.init_with_string(string)
            self.assertEqual("pac", self.element.type)
            self.assertEqual(mod, self.element.modifier)
            self.assertEqual(name, self.element.package.name)
            self.assertEqual(version, self.element.package.version)

    def test_get_value_pac(self):
        self.element.init_with_string("+ pac a")
        self.assertIsInstance(self.element.get_value(), package_config.Package)

    def test_get_value_tag(self):
        self.element.init_with_string("+ tag a")
        self.assertEqual(self.element.get_value(), "a")

    def test_get_value_fail(self):
        self.element.init_with_string("+ all")
        self.assertRaises(Exception, self.element.get_value)
