import unittest
from lib.util.io import PacupUserError
from lib.configuration.configuration import Configuration
from lib.configuration.tagged_package_list import TaggedPackageList

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.config = Configuration()
    def test_init_with_file_content(self):
        self.config.init_with_file_content(
            """

            + all

            - tag a

            + tag b


            + pac pa@1.2 

            - pac pb@2.1
            
            + pac pbdf
            """
        )
        self.assertEqual(6, len(self.config.configuration_elements))
        self.assertEqual("pa", self.config.configuration_elements[3].package.name)
        self.assertEqual("pac", self.config.configuration_elements[5].type)
        self.assertEqual("-", self.config.configuration_elements[4].modifier)

    def test_get_matching_packages_tags(self):
        package_list = TaggedPackageList()
        package_list.init_with_file_content(
            """
            a gaming
            b gaming coding
            b@2 coding
            c gaming
            """
        )
        self.config.init_with_file_content(
            """
            + all
            - tag coding
            """
        )
        packages = self.config.get_matching_packages(package_list)
        self.assertEqual(2, len(packages))

    def test_get_matching_packages_pacs(self):
        package_list = TaggedPackageList()
        package_list.init_with_file_content(
            """
            a gaming
            b gaming coding
            b@2 coding
            c gaming
            """
        )
        self.config.init_with_file_content(
            """
            + all
            - pac b
            """
        )
        packages = self.config.get_matching_packages(package_list)
        self.assertEqual(3, len(packages))

    def test_get_matching_packages_pacs_version(self):
        package_list = TaggedPackageList()
        package_list.init_with_file_content(
            """
            a gaming
            b gaming coding
            b@2 coding
            c gaming
            """
        )
        self.config.init_with_file_content(
            """
            + all
            - pac b@2
            """
        )
        packages = self.config.get_matching_packages(package_list)
        self.assertEqual(3, len(packages))

    def test_get_matching_packages_addpac(self):
        package_list = TaggedPackageList()
        package_list.init_with_file_content(
            """
            a gaming
            b gaming coding
            b@2 coding
            c gaming
            """
        )
        self.config.init_with_file_content(
            """
            + pac b
            - pac b@2
            """
        )
        packages = self.config.get_matching_packages(package_list)
        self.assertEqual(1, len(packages))

    def test_get_matching_packages_invalid(self):
        package_list = TaggedPackageList()
        package_list.init_with_file_content(
            """
            a gaming
            b gaming coding
            b@2 coding
            c gaming
            """
        )
        self.config.init_with_file_content(
            """
            + all
            """
        )
        def test():
            self.config.get_matching_packages(package_list)
        self.assertRaises(PacupUserError, test)

    def test_get_matching_packages_invalid_tag(self):
        package_list = TaggedPackageList()
        package_list.init_with_file_content(
            """
            a gaming
            b gaming coding
            b@2 coding
            c gaming
            """
        )
        self.config.init_with_file_content(
            """
            - tag sdf
            """
        )
        packages = self.config.get_matching_packages(package_list)
        self.assertEqual(0, len(packages))
