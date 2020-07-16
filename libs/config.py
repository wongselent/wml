import json
import os
import sys
from typing import List, Tuple, Dict, Callable

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
except AttributeError:
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

    __str: Dict[int, str] = {
        R144P: "144p",
        R240P: "240p",
        R360P: "360p",
        R480P: "480p",
        R720P: "720p",
        R1080P: "1080p"
    }

    __resolution: Dict[int, tuple] = {
        R144P: (256, 144),
        R240P: (426, 240),
        R360P: (640, 360),
        R480P: (854, 480),
        R720P: (1280, 720),
        R1080P: (1920, 1080)
    }

    @classmethod
    def str(cls, value: int) -> str:
        return cls.__str.get(value)

    @classmethod
    def resolution(cls, value: int) -> tuple:
        return cls.__resolution.get(value)


class SOCIAL_TYPES:
    IG: int = 0
    TT: int = 1
    TW: int = 3
    FB: int = 4

    __code: Dict[int, str] = {
        IG: "ig",
        TT: "tt",
        TW: "tw",
        FB: "fb"
    }

    __str: Dict[int, str] = {
        IG: "instagram",
        TT: "tiktok",
        TW: "twitter",
        FB: "facebook"
    }

    @classmethod
    def code(cls, value: int) -> str:
        return cls.__code.get(value)

    @classmethod
    def str(cls, value: int) -> str:
        return cls.__str.get(value)


class MEDIA_TYPES:
    PIC: int = 0
    VID: int = 1

    __code: Dict[int, str] = {
        PIC: "pic",
        VID: "vid"
    }

    __str: Dict[int, str] = {
        PIC: "picture",
        VID: "video"
    }

    @classmethod
    def code(cls, value: int) -> str:
        return cls.__code.get(value)

    @classmethod
    def str(cls, value: int) -> str:
        return cls.__str.get(value)


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
        #TODO: cannot get variable in SOCIAL_TYPES class
        json.dump(SOCIAL_TYPES._pattern, f, indent=4)


def read_wml_setup_file() -> Dict:
    with open(WML_SETUP_FILE, "r") as f:
        return json.load(f)


def set_string_to_list(value: str, sep: str = ";") -> List[str]:
    if not value:
        return list()
    return [v.strip() for v in value.split(sep) if v]


def set_plaintext_to_list(form_obj: QtWidgets.QPlainTextEdit) -> List[str]:
    if not form_obj.isEnabled():
        return list()

    form_list: List[str] = set_string_to_list(form_obj.toPlainText())
    return form_list
