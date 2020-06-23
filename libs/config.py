import json
import os
import sys
from typing import List, Tuple, Dict, Union, Callable

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi


def join_directory(*args, cwd_path: bool = False) -> str:
    path: list = [*args]

    if cwd_path:
        path.insert(0, CWD_PATH)

    return os.path.join(*path).replace("\\", "/")


PPREFIX: str = "wml"
SUFFIX: str = ""
VIDEO_FPS = 60

try:
    BASE_PATH: str = sys._MEIPASS
except:
    BASE_PATH: str = os.getcwd()

CWD_PATH: str = os.path.dirname(os.getcwd())

ASSETS_PATH: str = join_directory(BASE_PATH, "assets")
UI_PATH: str = join_directory(ASSETS_PATH, "ui")
TEMP_PATH: str = join_directory(f"{PPREFIX}-temp", cwd_path=True)  # wml-temp
ENV_PATH: str = join_directory(f"{PPREFIX}-env", cwd_path=True)  # wml-env

BUILD_PATH: str = join_directory(f"{PPREFIX}-build", cwd_path=True)
BUILD_BUILD_PATH: str = join_directory(BUILD_PATH, "build")
BUILD_DIST_PATH: str = join_directory(BUILD_PATH, "dist")

OUTPUT_PATH: str = join_directory(f"{PPREFIX}-output", cwd_path=True)  # wml-output
OUTPUT_DATA_PATH: str = join_directory(OUTPUT_PATH, ".data")  # wml-output/.data

VIDEO_PATH: str = join_directory(f"{PPREFIX}-video", cwd_path=True)  # wml-video

WML_SETUP_FILE: str = f"{CWD_PATH}/{PPREFIX}-setup.json"  # wml-setup.json
WML_CONDA_ENV_FILE: str = f"{ENV_PATH}/{PPREFIX}-conda-env.yml"
WML_PIP_REQUIREMENT_FILE: str = f"{ENV_PATH}/{PPREFIX}-pip-requirement.txt"

# VIDEO_WIDTH, VIDEO_HEIGHT = 1280, 720

FILENAME_PATTERN = f"{PPREFIX}__{{social}}__{{looter}}__{{media_type}}__{{username}}__{{name}}"


class VIDEO_RESOLUTION:
    R144P = 0
    R240P = 1
    R360P = 2
    R480P = 3
    R720P = 4
    R1080P = 5

    _str: Dict[int, str] = {
        R144P: "144p",
        R240P: "240p",
        R360P: "360p",
        R480P: "480p",
        R720P: "720p",
        R1080P: "1080p"
    }

    _resolution: Dict[int, tuple] = {
        R144P: (256, 144),
        R240P: (426, 240),
        R360P: (640, 360),
        R480P: (854, 480),
        R720P: (1280, 720),
        R1080P: (1920, 1080)
    }

    @classmethod
    def str(cls, value: int) -> str:
        return cls._str[value]

    @classmethod
    def resolution(cls, value: int) -> tuple:
        return cls._resolution[value]


class SOCIAL_TYPES:
    IG: int = 0
    TT: int = 1
    TW: int = 3
    FB: int = 4

    _code: dict = {
        IG: "ig",
        TT: "tt",
        TW: "tw",
        FB: "fb"
    }

    _str: dict = {
        IG: "instagram",
        TT: "tiktok",
        TW: "twitter",
        FB: "facebook"
    }

    _pattern: dict = {
        "active_setup": {
            "instagram": 1,
            "twitter": 0,
            "tiktok": 0,
            "facebook": 0
        },
        "accounts_setup": {
            "instagram": {
                "login": {
                    "username": "---",
                    "password": "---"
                },
                "options": {}
            },
            "twitter": {
                "login": {
                    "username": "---",
                    "password": "---"
                },
                "options": {}
            },
            "tiktok": {
                "login": {
                    "username": "---",
                    "password": "---"
                },
                "options": {}
            },
            "facebook": {
                "login": {
                    "username": "---",
                    "password": "---"
                },
                "options": {}
            },
            "youtube": {
                "login": {
                    "username": "---",
                    "password": "---"
                },
                "options": {
                    "subscribe_video_path": None,
                    "subscribe_video_show_every": 5  # minute
                }
            }
        },
        "looters_setup": {
            "instagram": {
                "profile": {
                    "list": ["profile1", "profile2"],
                    "type": ["picture", "video"],
                    "count": 10
                },
                "hashtag": {
                    "list": ["#baby", "#people"],
                    "type": ["picture", "video"],
                    "count": 10
                },
                "top_search": {
                    "type": ["picture", "video"],
                    "count": 10
                }
            },
            "twitter": {},
            "tiktok": {},
            "facebook": {}
        },
        "render_setup": {
            "intro_video_path": "---",
            "outro_video_path": "---",
        },
        "upload_setup": {},
        "options": {
            "all_count": None,
            "all_type": None
        }
    }


class MEDIA_TYPES:
    PIC: int = 0
    VID: int = 1

    _code: Dict[int, str] = {
        PIC: "pic",
        VID: "vid"
    }

    _str: Dict[int, str] = {
        PIC: "picture",
        VID: "video"
    }


def create_directory(path: str) -> bool:
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False


# def create_temp_directory() -> None:
#     _dir = TemporaryDirectory(prefix=f"{PPREFIX}_")
#     _dir.write()

def load_ui(baseinstance: QtWidgets.QWidget = None) -> str:
    ui_name = f"{os.path.basename(baseinstance.__class__.__name__)}.ui"
    ui_file = join_directory(UI_PATH, ui_name)

    return loadUi(ui_file, baseinstance=baseinstance)


def append_widget(layout: QtWidgets.QLayout, widgets: Tuple[QtWidgets.QWidget] = None) -> Tuple[QtWidgets.QWidget]:
    for widget in widgets:
        layout.addWidget(widget)

    return widgets


def set_disabled_widgets(*widgets: Tuple[QtWidgets.QWidget], state: bool = True) -> Callable[[bool], None]:
    def _set_disabled_widgets(st: bool) -> None:
        for widget in widgets:
            widget: QtWidgets.QWidget
            widget.setDisabled(st)

    _set_disabled_widgets(state)
    return _set_disabled_widgets


def create_wml_setup_file() -> None:
    with open(WML_SETUP_FILE, "w") as f:
        json.dump(SOCIAL_TYPES._pattern, f, indent=4)


def read_wml_setup_file() -> Dict:
    with open(WML_SETUP_FILE, "r") as f:
        return json.load(f)


def set_string_to_list(value: str, sep: str = ";") -> List[str]:
    return [v.strip() for v in value.split(sep)]
