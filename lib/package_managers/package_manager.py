import os, subprocess

from ..util import package
from ..util.package import Package
from ..util.output import PacupUserError

PACMANDIR = os.path.abspath(os.path.dirname(__file__))

def get_package_manager_names():
    names = []
    for entry in os.listdir(PACMANDIR):
        if os.path.isdir(os.path.join(PACMANDIR, entry)) and \
           entry != "__pycache__":
            names.append(entry)
    names.sort()
    return names

def run_command(cmd):
    res = subprocess.run(
        cmd,
        capture_output=True,
        shell=True
    )
    exitcode = res.returncode
    stdout = res.stdout.decode('utf-8')
    stderr = res.stderr.decode('utf-8')
    return exitcode, stdout, stderr

def run_command_interactive(cmd):
    res = subprocess.run(
        cmd,
        shell=True
    )
    exitcode = res.returncode
    return exitcode

class PackageManager:
    valid_package_managers = get_package_manager_names()

    def __init__(self, name):
        assert(name in PackageManager.valid_package_managers)
        self.name = name

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
        return "{}/{}".format(PACMANDIR, self.name)

    def is_installed(self) -> bool:
        if hasattr(self, "is_installed_cache"): return self.is_installed_cache
        exitcode,_,_ = run_command("{}/exists.sh".format(self._get_path()))
        self.is_installed_cache = exitcode == 0
        return self.is_installed_cache

    def get_installed_packages(self) -> list[Package]:
        # TODO cache?
        exitcode,stdout,_ = run_command("{}/get.sh".format(self._get_path()))
        assert(exitcode == 0)
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
            raise PacupUserError("while installing with {} an error for package: {}".format(self.name, package))
        if exitcode == 2:
            raise PacupUserError("{} does not support installing specific a version".format(self.name))
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
