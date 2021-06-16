import sys
from .tagged_package_list import TaggedPackageListFactory

list_path = sys.argv[1]
output_path = sys.argv[2]

package_list = TaggedPackageListFactory.create_list_from_filename(list_path)
for line in sys.stdin.readlines():
    if len(line.split()) == 2: line = line.split()[0]+"@"+line.split()[1]
    package_list.append_str(line)
package_list.write_to_file(output_path)
