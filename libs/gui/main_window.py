from .. import config
from .components import tabbar_widget, social_widget, form_widget

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabBar, QTabWidget

from PyQt5 import QtWidgets, QtGui

import sys

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        config.load_ui(self)
        
        self.setWindowTitle("WML v0.1.0: Nasilotek")
        self.main_tabwidget.setTabText(0, "WML")
        # self.main_tabwidget.setTabsClosable(True)
        
        self.__main_tab = tabbar_widget.TabBar(self.main_tabwidget, "WML",)
        self.__social_looter_tab = tabbar_widget.TabBar(self.main_tabwidget, "Social Looter")
        self.__create_video_tab = tabbar_widget.TabBar(self.main_tabwidget, "Create Video")

        self.__social_looter_tab.addWidget(social_widget.SocialLooterWidget(self))
        self.__create_video_tab.addWidget(social_widget.CreateVideoWidget(self))

        # self.__test()

    def addWidget(self, widget: QWidget) -> None:
        self.main_window_layout.addWidget(widget)

    def __test(self):
        from libs import video_editor as veditor

        rd = veditor.RenderVideo("/home/wongselent/Videos/memes_1", bg_blur=True)
        rd.setSize(width=1280, height=720, reduce=3)

        label = QtWidgets.QLabel(self)
        image = rd.getFrameImage(label)

        btn = QtWidgets.QPushButton("next", self)
        btn.clicked.connect(lambda: next(image))

        self.addWidget(label)
        self.addWidget(btn)

def run(argv: list =[]):
    if len(argv) > 1: sys.exit(argv)

    app: QApplication = QApplication(argv)
    win: QMainWindow = MainWindow()
    win.show()
    sys.exit(app.exec_())

