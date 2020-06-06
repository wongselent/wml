from libs import config, video_editor
from libs.socials import instagram

import os
import sys

# prepare setup tool
prepare_paths: list = [
    config.TEMP_PATH,
    config.BUILD_PATH,
    config.ENV_PATH,
    config.OUTPUT_DATA_PATH,
    config.VIDEO_RENDER_PATH,
    config.VIDEO_FINISH_PATH,
    config.VIDEO_ERROR_PATH,
    config.VIDEO_UPLOAD_PATH
]

for path in prepare_paths:
    config.create_directory(path)

if not os.path.exists(config.WML_SETUP_FILE):
    config.create_wml_setup_file()


config.read_wml_setup_file()

# instagram.loot_profile("memes.video", loot_type=1, loot_max_count=20, loot_total_count=200)

# video_editor.create_video("/home/wongselent/Videos/memes_1")

# print(config.BASE_PATH, config.CWD_PATH)
# print(os.path.isfile(config.join_directory(config.ASSETS_PATH, "logo.jpg")))

from libs.gui import main_window
main_window.run(argv=sys.argv)

# def imgClip():
#     from moviepy.editor import ImageClip
#     from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtMultimediaWidgets
#     img_clip = ImageClip("/home/wongselent/Downloads/4.1.png")

#     app = QtWidgets.QApplication(argv)

#     player = QtMultimedia.QMediaPlayer()
#     player.setMedia(QtMultimedia.QMediaContent())
#     sys.exit(app.exec_())

# print( imgClip(), type(imgClip()) )