from PyQt5 import QtCore, QtWidgets

import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()