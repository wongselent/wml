from libs import tool, setting, video_editor
from libs.socials import instagram

import os
import sys

# # prepare setup tool
# prepare_paths: list = [
#     setting.TEMP_PATH,
#     setting.BUILD_PATH,
#     setting.ENV_PATH,
#     setting.OUTPUT_DATA_PATH,
#     setting.VIDEO_RENDER_PATH,
#     setting.VIDEO_FINISH_PATH,
#     setting.VIDEO_ERROR_PATH,
#     setting.VIDEO_UPLOAD_PATH
# ]

# for path in prepare_paths:
#     tool.create_directory(path)

# if not os.path.exists(setting.WML_SETUP_FILE):
#     tool.create_wml_setup_file()


# tool.read_wml_setup_file()

# instagram.loot_profile("memes.video", loot_type=1, loot_max_count=20, loot_total_count=200)

# video_editor.create_video("/home/wongselent/Videos/memes_1")

# print(setting.BASE_PATH, setting.CWD_PATH)
# print(os.path.isfile(setting.join_directory(setting.ASSETS_PATH, "logo.jpg")))

from libs.gui import runGui

runGui(argv=sys.argv)