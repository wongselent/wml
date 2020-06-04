from .. import setting
from .components import tabbar, form

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabBar, QTabWidget

import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        setting.load_ui(__file__, self)

        self.setWindowTitle("WML v0.1.0: Nasilotek")
        self.main_tabwidget.setTabText(0, "WML")
        # self.main_tabwidget.setTabsClosable(True)
        
        self.__main_tab: QTabBar = tabbar.TabBar("WML", self.main_tabwidget)
        self.__main_tab: QTabBar = tabbar.TabBar("Page 1", self.main_tabwidget)

        f = form.Form("instagram", "username", self)

        self.verticalLayout.addWidget(f)


def run(argv: list =[]):
    if len(argv) > 1: sys.exit(argv)

    app: QApplication = QApplication(argv)
    win: QMainWindow = MainWindow()
    win.show()
    sys.exit(app.exec_())