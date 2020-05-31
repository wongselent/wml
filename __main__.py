from libs import tool, setting
from libs import instagram

import os

# prepare setup tool
prepare_paths: list = [
    setting.TEMP_PATH,
    setting.BUILD_PATH,
    setting.ENV_PATH,
    setting.OUTPUT_DATA_PATH,
    setting.VIDEO_RENDER_PATH,
    setting.VIDEO_FINISH_PATH,
    setting.VIDEO_ERROR_PATH,
    setting.VIDEO_UPLOAD_PATH
]

for path in prepare_paths:
    tool.create_directory(path)

if not os.path.exists(setting.WML_SETUP_FILE):
    tool.create_wml_setup_file()


tool.read_wml_setup_file()

instagram.loot_hashtag("cat", loot_type=0, loot_count=1)