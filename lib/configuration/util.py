import os

def get_list_path(pacmanname) -> str:
    dirname=os.path.expanduser("~/.config/pacup/lists")
    if "PACUP_LISTS_DIR" in os.environ:
        dirname=os.environ["PACUP_LISTS_DIR"]
    filename="{}.list".format(pacmanname)
    return os.path.join(dirname, filename)

def get_config_path(pacmanname) -> str:
    dirname=os.path.expanduser("~/.config/pacup/configs")
    if "PACUP_CONFIGS_DIR" in os.environ:
        dirname=os.environ["PACUP_CONFIGS_DIR"]
    filename="{}.conf".format(pacmanname)
    return os.path.join(dirname, filename)
