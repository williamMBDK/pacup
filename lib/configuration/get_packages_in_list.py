import sys
from .tagged_package_list import TaggedPackageListFactory
from .package import TaggedPackage

list_path = sys.argv[1]

package_list = TaggedPackageListFactory.create_list_from_filename(list_path)
for pac in package_list.tagged_packages:
    print(super(TaggedPackage, pac).__str__())
