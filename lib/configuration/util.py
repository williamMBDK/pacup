from .configuration import ConfigurationFactory
from .tagged_package_list import TaggedPackageListFactory, TaggedPackageList
from ..util.output import PacupUserError

def append_to_package_list(
    input_list_path : str,
    output_list_path : str,
    packages : list[str]
):
    package_list = TaggedPackageListFactory.create_list_from_filename(input_list_path)
    for line in packages:
        package_list.append_str(line)
    package_list.write_to_file(output_list_path)

def get_matching_packages(config_path, paclist_path):
    config = None
    taggedlist = TaggedPackageList()

    try: config = ConfigurationFactory.create_configuration_from_filename(config_path)
    except FileNotFoundError: raise PacupUserError("config path does not exist")
    except IsADirectoryError: raise PacupUserError("config path is a directory")
    except ValueError: raise PacupUserError("invalid syntax in config")

    try: taggedlist = TaggedPackageListFactory.create_list_from_filename(paclist_path)
    except FileNotFoundError: raise PacupUserError("package list path does not exist")
    except IsADirectoryError: raise PacupUserError("package list path is a directory")
    except ValueError: raise PacupUserError("invalid syntax in package list")

    matched_packages = []
    try: matched_packages = config.get_matching_packages(taggedlist)
    except ValueError as e: raise PacupUserError("incomplete config: ", e)

    return matched_packages
