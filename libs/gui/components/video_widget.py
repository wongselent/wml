from PyQt5 import QtCore, QtWidgets

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

desktop = QtWidgets.QApplication.desktop()

player = QMediaPlayer()
player.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(r"/mnt/Resources/projects/python-project/wml-video/upload/memes_1.webm")))
video_widget = QVideoWidget()
video_widget.setGeometry(0 ,0, 1280, 720)
player.setVideoOutput(video_widget)
video_widget.show()

player.play()