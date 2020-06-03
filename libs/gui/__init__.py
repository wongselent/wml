from .. import tool

from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

def runGui(argv: list =[]):
    app: QApplication = QApplication(argv)
    win = QMainWindow()
    win.show()
    print(tool.get_ui_file(__file__))
    sys.exit(app.exec_())