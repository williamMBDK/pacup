import sys
from .tagged_package_list import TaggedPackageListFactory

list_path = sys.argv[1]
output_path = sys.argv[2]

to_add = sys.argv[3:]

package_list = TaggedPackageListFactory.create_list_from_filename(list_path)
for str_package_to_add in to_add:
    package_list.append_str(str_package_to_add)

package_list.write_to_file(output_path)
