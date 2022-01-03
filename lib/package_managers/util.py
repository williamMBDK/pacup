import os, subprocess, sys
from ..util.io import print_error

PACMANDIR = os.path.abspath(os.path.dirname(__file__))

def get_valid_package_managers_paths():
    name2path = {}
    for entry in os.listdir(PACMANDIR):
        dir=os.path.join(PACMANDIR, entry)
        if os.path.isdir(dir) and \
           entry != "__pycache__":
            name2path[entry] = dir
    if "PACUP_EXTRA_PMS" in os.environ:
        root_dir = os.environ["PACUP_EXTRA_PMS"]
        for entry in os.listdir(root_dir):
            dir=os.path.join(root_dir, entry)
            if os.path.isdir(dir):
                if entry in name2path:
                    print_error("A package manager in $PACUP_EXTRA_PMS has the same name as a supported package manager: {}"
                        .format(entry)
                    )
                    sys.exit(1)
                name2path[entry] = dir
    return name2path

valid_package_managers_paths = get_valid_package_managers_paths()
valid_package_manager_names = list(valid_package_managers_paths.keys())
valid_package_manager_names.sort()

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
