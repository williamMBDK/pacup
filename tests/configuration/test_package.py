import unittest
from configuration.package import Package, TaggedPackage

class TestPackage(unittest.TestCase):

    def setUp(self):
        self.package = Package()

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
            self.package = Package()
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
            self.package = Package()
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
        self.package = TaggedPackage()

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
            self.package = TaggedPackage()
            self.package.init_with_string(string) 
            self.assertEqual(expected, self.package.tags)
