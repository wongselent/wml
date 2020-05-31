from . import setting

from addict import Dict

import os
import json

def create_directory(path: str) -> bool:
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

# def create_temp_directory() -> None:    
#     _dir = TemporaryDirectory(prefix=f"{PPREFIX}_")
#     _dir.write()

def join_directory(*args, cwd_path: bool =False) -> str:
    path: list = [*args]
    
    if cwd_path:
        path.insert(0, setting.CWD_PATH)

    return os.path.join(*path).replace("\\", "/")

def create_wml_setup_file() -> None:
    with open(setting.WML_SETUP_FILE, "w") as f:
        json.dump(setting.SOCIAL_TYPES._pattern, f, indent=4)

def read_wml_setup_file() -> Dict:
    with open(setting.WML_SETUP_FILE, "r") as f:
        return Dict(json.load(f))