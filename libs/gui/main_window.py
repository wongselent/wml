import sys
from typing import Dict

from PyQt5 import QtCore, QtWidgets

from libs import config, thread
from libs.gui.components import tabbar_widget, video_widget, social_widget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        config.load_ui(self)
        self.thread_pool: QtCore.QThreadPool = thread.ThreadPool(parent=self)

        self.setWindowTitle("WML v0.1.0: Nasilotek")
        self.main_tabwidget.setTabText(0, "WML")
        # self.main_tabwidget.setTabsClosable(True)

        self.__social_looter_tab = tabbar_widget.TabBar(
            parent=self.main_tabwidget,
            tab_title="Instagram Looter",
            tab_widget=social_widget.InstagramLooterWidget(self)
        )

        self.__create_video_tab = tabbar_widget.TabBar(
            parent=self.main_tabwidget,
            tab_title="Create Video",
            tab_widget=video_widget.CreateVideoWidget(parent=self, threadpool_obj=self.thread_pool)
        )

    def closeEvent(self, event) -> None:
        pass


def run(argv: Dict[str, str] = None) -> None:
    if len(argv) > 1:
        sys.exit(argv)

    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())
