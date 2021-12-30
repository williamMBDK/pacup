import os

def get_configs_dir() -> str:
    dirname=os.path.expanduser("~/.config/pacup/configs")
    if "PACUP_CONFIGS_DIR" in os.environ:
        dirname=os.environ["PACUP_CONFIGS_DIR"]
    return dirname

def get_config_path(pacmanname) -> str:
    filename="{}.conf".format(pacmanname)
    return os.path.join(get_configs_dir(), filename)

def get_lists_dir() -> str:
    dirname=os.path.expanduser("~/.config/pacup/lists")
    if "PACUP_LISTS_DIR" in os.environ:
        dirname=os.environ["PACUP_LISTS_DIR"]
    return dirname

def get_list_path(pacmanname) -> str:
    filename="{}.list".format(pacmanname)
    return os.path.join(get_lists_dir(), filename)
