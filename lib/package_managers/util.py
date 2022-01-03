from . import package_manager

def get_package_managers():
    return [
        package_manager.PackageManager(pacman)
        for pacman in package_manager.PackageManager.valid_package_manager_names
    ]
