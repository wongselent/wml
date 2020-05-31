from addict import Dict

from .tool import join_directory

import os
import sys

PPREFIX: str = "wml"
SUFFIX: str = ""

try:
    BASE_PATH: str = sys._MEIPASS
    CWD_PATH: str = os.getcwd()
except:
    BASE_PATH: str = os.path.dirname(os.getcwd())
    CWD_PATH: str = BASE_PATH

TEMP_PATH: str = join_directory(f"{PPREFIX}-temp", cwd_path=True)               # wml-temp
ENV_PATH: str = join_directory(f"{PPREFIX}-env", cwd_path=True)                 # wml-env

BUILD_PATH: str = join_directory(f"{PPREFIX}-build", cwd_path=True)
BUILD_BUILD_PATH: str = join_directory(BUILD_PATH, "build")
BUILD_DIST_PATH: str = join_directory(BUILD_PATH, "dist")

OUTPUT_PATH: str = join_directory(f"{PPREFIX}-output", cwd_path=True)           # wml-output
OUTPUT_DATA_PATH: str = join_directory(OUTPUT_PATH, ".data")                    # wml-output/.data

VIDEO_PATH: str = join_directory(f"{PPREFIX}-video", cwd_path=True)             # wml-video
VIDEO_RENDER_PATH: str = join_directory(VIDEO_PATH, "render")                   # wml-video/.render
VIDEO_FINISH_PATH: str = join_directory(VIDEO_PATH, "finish")                   # wml-video/.finish
VIDEO_ERROR_PATH: str = join_directory(VIDEO_PATH, "error")                     # wml-video/.error
VIDEO_UPLOAD_PATH: str = join_directory(VIDEO_PATH, "upload")                   # wml-video/.upload

WML_SETUP_FILE: str = f"{CWD_PATH}/{PPREFIX}-setup.json"                        # wml-setup.json
WML_CONDA_ENV_FILE: str = f"{ENV_PATH}/{PPREFIX}-conda-env.yml"
WML_PIP_REQUIREMENT_FILE: str = f"{ENV_PATH}/{PPREFIX}-pip-requirement.txt"

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

    _url: dict = {}

    _dir: dict = {
        IG: {
            "profile": join_directory(OUTPUT_PATH, _str[IG], "profile"),
            "hashtag": join_directory(OUTPUT_PATH, _str[IG], "hastag")
        }
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
                    "subscribe_video_show_every": 5 # minute
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

    _code: dict = {
        PIC: "pic",
        VID: "vid"
    }
    
    _str: dict = {
        PIC: "picture",
        VID: "video"
    }
