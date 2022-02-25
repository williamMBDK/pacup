from .configuration.tagged_package import TaggedPackageFactory
from .configuration.tagged_package_list import TaggedPackageListFactory
from .util.io import lazy_confirm, print_green, print_needed_info, print_normal, print_success
from .package_managers.package_manager import PackageManager

def handler(args):
    for i,pm in enumerate(args.package_managers):
        if i > 0: print_normal()
        backup_into_package_manager_list(args, pm)

def backup_into_package_manager_list(args, pm : PackageManager):
    list_path = None
    if pm.has_list(): list_path = pm.get_list_path()
    if args.list != None: list_path = args.list
    assert(list_path != None)
    explicits = pm.get_installed_packages()
    tagged_list = pm.get_list()
    pacs_to_add = []
    for full_pac in explicits:
        pac = full_pac if args.with_version else full_pac.without_version()
        if not tagged_list.contains(pac):
            if args.interactive and \
               not lazy_confirm("Do you wish to add the following package to the package-list: {}".format(pac)):
                # TODO should --yes do something here?
                print_needed_info("Skipping {}".format(pac))
                continue
            pacs_to_add.append(pac)
    if len(pacs_to_add) == 0:
        if args.verbosity >= 1: print_needed_info("Nothing to backup for {}".format(pm.name))
        return
    if args.verbosity >= 1:
        print_needed_info("Packages installed but not in package list ({})".format(list_path))
        for pac in pacs_to_add: print_green(pac)
        if not args.yes and not lazy_confirm("Do you wish to add the above packages to {}?".format(list_path)): return
    append_tagged_list = TaggedPackageListFactory.create_empty_list()
    for pac in pacs_to_add:
        tagged_pac = TaggedPackageFactory.create_tagged_package_from_values(
            pac.get_name(), pac.version, []
        )
        append_tagged_list.append(tagged_pac)
    append_tagged_list.append_to_file(list_path)
    if args.verbosity >= 1: print_success("Added packages to package-list ({})".format(list_path))
