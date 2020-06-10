from libs import config
from PyQt5 import QtCore, QtWidgets
from libs import config

import os
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt5.QtMultimediaWidgets import QVideoWidget

# desktop = QtWidgets.QApplication.desktop()

# player = QMediaPlayer()
# player.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(r"/mnt/Resources/projects/python-project/wml-video/upload/memes_1.webm")))
# video_widget = QVideoWidget()
# video_widget.setGeometry(0 ,0, 1280, 720)
# player.setVideoOutput(video_widget)
# video_widget.show()

# player.play()


class VideoPreviewWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget):
        super(VideoPreviewWidget, self).__init__(parent)
        config.load_ui(self)

        self.__parent = parent
        self.__video_data: dict = {}

class VideoItemWidget(object):
    def __init__(self, parent: QtWidgets.QListWidget, video_name: str = None, video_files: list = None):
        super(VideoItemWidget, self).__init__(parent)
        config.load_ui(self)

        self.__parent  = parent
        self.__video_name = video_name
        self.__video_files = video_files

        self.title_label: QtWidgets.QLabel
        self.render_progressbar: QtWidgets.QProgressBar
        self.render_info_label: QtWidgets.QLabel
        self.preview_button: QtWidgets.QPushButton
        self.render_button: QtWidgets.QPushButton


class CreateVideoWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(CreateVideoWidget, self).__init__(parent)
        config.load_ui(self)

        self.__parent = parent
        self.video_path_edit: QtWidgets.QLineEdit
        self.video_intro_edit: QtWidgets.QLineEdit
        self.video_outro_edit: QtWidgets.QLineEdit
        self.video_path_button: QtWidgets.QPushButton
        self.intro_path_button: QtWidgets.QPushButton
        self.outro_path_button: QtWidgets.QPushButton
        self.render_all_button: QtWidgets.QPushButton
        self.video_obj_list: QtWidgets.QListWidget

        self.video_path_button.clicked.connect(self.getVideoPath)
        self.intro_path_button.clicked.connect(self.getIntroPath)
        self.outro_path_button.clicked.connect(self.getOutroPath)

    def getVideoPath(self):
        video_data: dict = {}

        root_path = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Video Path",
            directory="/"
        )

        self.video_path_edit.setText(root_path)

        for dirpath, dirnames, filenames, in os.walk(root_path):
            for dirname in dirnames:
                video_path = config.join_directory(dirpath, dirname)
                video_data[video_path] = []
                for filename in os.listdir(video_path):
                    video_file = config.join_directory(video_path, filename)
                    if os.path.isfile(video_file):
                        _, ext = os.path.splitext(video_file)
                        if ext.lower() in (".mp4", ".webm"):
                            video_data[video_path].append(video_file)

        if video_data:
            self.__createVideoItemWidget(video_data)

        self.__video_data = video_data

        return video_data


    def getIntroPath(self):
        root_path = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Intro Path",
            directory="/",
            filter="Video Ext (*.mp4 *.webm)"
        )

        self.video_intro_edit.setText(root_path)

    
    def getOutroPath(self):
        root_path = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Intro Path",
            directory="/",
            filter="Video Ext (*.mp4 *.webm)"
        )

        self.video_outro_edit.setText(root_path)

    def __createVideoItemWidget(self, video_data):
        self.video_obj_list.appe


            

