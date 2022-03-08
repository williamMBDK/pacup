import os
from typing import Optional
from ..util import package
from ..util.package import Package
from ..util.io import PacupInstallError, PacupUnknownError
from ..configuration import get_config_path, get_list_path, Configuration, TaggedPackageList
from .util import run_command, run_command_interactive, valid_package_managers_paths, valid_package_manager_names

class PackageManager:

    def __init__(self, name):
        assert(name in valid_package_managers_paths)
        self.name = name
        self.config : Optional[Configuration] = None
        self.list : Optional[TaggedPackageList] = None

    def __eq__(self, other):
        if isinstance(other, PackageManager):
            return self.name == other.name
        return False

    def __ne__(self, other):
        if isinstance(other, PackageManager):
            return self.name != other.name
        return True

    def __str__(self):
        return self.name

    def _get_path(self):
        return valid_package_managers_paths[self.name]

    def is_installed(self) -> bool:
        if hasattr(self, "is_installed_cache"): return self.is_installed_cache
        exitcode,_,_ = run_command("{}/exists.sh".format(self._get_path()))
        self.is_installed_cache = exitcode == 0
        return self.is_installed_cache

    def get_installed_packages(self) -> list[Package]:
        # TODO cache?
        cmd="{}/get.sh".format(self._get_path())
        exitcode,stdout,_ = run_command(cmd)
        if exitcode != 0: raise PacupUnknownError("an error occurred when listing explicit packages from {}.\nThis may be your installation not working or an error in pacup.\nYou may try running {} to see what caused the error.".format(self.name, cmd))
        return [
            package.PackageFactory.create_package_from_string(line)
            for line in stdout.split()
        ]

    def install_package(self, package : Package):
        exitcode = run_command_interactive("{}/install.sh {}".format(
            self._get_path(), package.name
        )) if package.version == None else run_command_interactive(
            "{}/install.sh {}".format(
                self._get_path(),
                package.name,
                package.version
            )
        )
        if exitcode == 1:
            raise PacupInstallError("while installing with {} an error for package: {}".format(self.name, package))
        if exitcode == 2:
            raise PacupInstallError("{} does not support installing a specific version".format(self.name))
        assert(exitcode == 0)

    def is_package_installed(self, package):
        exitcode,_,_ = run_command("{}/pac-installed.sh {}".format(
            self._get_path(), package.name
        )) if package.version == None else run_command(
            "{}/pac-installed.sh {}".format(
                self._get_path(),
                package.name,
                package.version
            )
        )
        assert(exitcode == 0 or exitcode == 1)
        return exitcode == 0

    def has_config(self):
        return os.path.exists(get_config_path(self.name))

    def has_list(self):
        return os.path.exists(get_list_path(self.name))

    def get_config_path(self, do_assert=True):
        if do_assert: assert(self.has_config())
        return get_config_path(self.name)

    def get_list_path(self, do_assert=True):
        if do_assert: assert(self.has_list())
        return get_list_path(self.name)

    def set_config(self, config):
        self.config = config

    def set_list(self, list):
        self.list = list

    def get_config(self):
        assert(self.config != None)
        return self.config

    def get_list(self):
        assert(self.list != None)
        return self.list

    def is_ready(self):
        return self.is_installed() and self.has_config() and self.has_list()

def get_package_managers():
    return [
        PackageManager(pacman)
        for pacman in valid_package_manager_names
    ]
