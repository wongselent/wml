import sys
from typing import Dict

from PyQt5 import QtWidgets

from .components import tabbar_widget, video_widget
from .. import config


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        config.load_ui(self)

        self.setWindowTitle("WML v0.1.0: Nasilotek")
        self.main_tabwidget.setTabText(0, "WML")
        # self.main_tabwidget.setTabsClosable(True)

        # self.__main_tab = tabbar_widget.TabBar(
        #     parent=self.main_tabwidget,
        #     tab_title="WML",
        #     tab_widget=None
        # )

        # TODO: tab lagi dibuat
        # self.__social_looter_tab = tabbar_widget.TabBar(
        #     parent=self.main_tabwidget,
        #     tab_title="Social Looter",
        #     tab_widget=social_widget.SocialLooterWidget(self)
        # )

        self.__create_video_tab = tabbar_widget.TabBar(
            parent=self.main_tabwidget,
            tab_title="Create Video",
            tab_widget=video_widget.CreateVideoWidget(self)
        )


def run(argv: Dict[str, str] = None):
    if len(argv) > 1:
        sys.exit(argv)

    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    # def __test(self):
    #     from libs import video_editor as veditor
    #
    #     rd = veditor.RenderVideo("/home/wongselent/Videos/memes_1", bg_blur=True)
    #     rd.setSize(width=1280, height=720, reduce=3)
    #
    #     label = QtWidgets.QLabel(self)
    #     image = rd.getFrameImage(label)
    #
    #     btn = QtWidgets.QPushButton("next", self)
    #     btn.clicked.connect(lambda: next(image))
    #
    #     self.addWidget(label)
    #     self.addWidget(btn)
