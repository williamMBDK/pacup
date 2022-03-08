import os
from typing import Optional

def get_configs_dir() -> str:
    dirname=os.path.expanduser("~/.config/pacup/configs")
    if "PACUP_CONFIGS_DIR" in os.environ:
        dirname=os.environ["PACUP_CONFIGS_DIR"]
    return dirname

def get_config_path(pacmanname) -> str:
    general_config=get_general_config()
    if general_config != None:
        return general_config
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

def remove_comments(line):
    try:
        idx = line.index('#')
        return line[:idx]
    except:
        return line

def get_general_config() -> Optional[str]:
    dir = get_configs_dir()
    general_config_path = os.path.join(dir, "all.conf")
    if os.path.exists(general_config_path):
        return general_config_path
    else:
        return None
