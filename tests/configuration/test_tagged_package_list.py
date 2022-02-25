from lib.util.io import PacupUserError
import unittest
from lib.configuration.tagged_package_list import TaggedPackageList
from lib.util.package import PackageFactory

class TestTaggedPackageList(unittest.TestCase):
    def setUp(self):
        self.package_list = TaggedPackageList()

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
        except PacupUserError:
            err = True
        self.assertTrue(err)

    def test_contains(self):
        self.package_list.init_with_file_content(
            """
            a@1
            a
            c@1
            """
        )
        self.assertTrue(self.package_list.contains(PackageFactory.create_package_from_values("a", "1")))
        self.assertTrue(self.package_list.contains(PackageFactory.create_package_from_values("a", None)))
        self.assertTrue(self.package_list.contains(PackageFactory.create_package_from_values("c", "1")))
        self.assertFalse(self.package_list.contains(PackageFactory.create_package_from_values("b", "1")))
        self.assertFalse(self.package_list.contains(PackageFactory.create_package_from_values("b", None)))
        self.assertFalse(self.package_list.contains(PackageFactory.create_package_from_values("a", "2")))

    def test_str(self):
        self.package_list.init_with_file_content(
            """
            c@3 tag
            b@2
            a@2 e f g a
            a@1 e f g a
            """
        )
        str(self.package_list)
        self.assertEqual("a", self.package_list.tagged_packages[0].name)
        self.assertEqual("a", self.package_list.tagged_packages[1].name)
        self.assertEqual("b", self.package_list.tagged_packages[2].name)
        self.assertEqual("c", self.package_list.tagged_packages[3].name)
        self.assertEqual("1", self.package_list.tagged_packages[0].version)
        self.assertEqual("2", self.package_list.tagged_packages[1].version)

    def test_append(self):
        self.package_list.init_with_file_content(
            """
            c@3 tag
            b@2
            a@2 e f g a
            a@1 e f g a
            """
        )
        self.package_list.append_str("d")
        self.assertEqual('d', self.package_list.tagged_packages[-1].name)
        self.package_list.append_str("c@2")
        self.assertEqual('c', self.package_list.tagged_packages[-1].name)

    def test_append_fail(self):
        self.package_list.init_with_file_content(
            """
            c@3 tag
            b@2
            a@2 e f g a
            a@1 e f g a
            """
        )
        def test():
            self.package_list.append_str("b@2")
        self.assertRaises(PacupUserError, test)

    def test_comments(self):
        self.package_list.init_with_file_content(
            """
            a@1 e f g a # this is a comment

            # hello
            # hello 123
            b@2#comment 
            c@3 tag# hey there
            # hello 123
            """
        )
        self.assertEqual(3, len(self.package_list.tagged_packages))
        self.assertEqual("a", self.package_list.tagged_packages[0].name)
        self.assertEqual("b", self.package_list.tagged_packages[1].name)
        self.assertEqual("c", self.package_list.tagged_packages[2].name)
