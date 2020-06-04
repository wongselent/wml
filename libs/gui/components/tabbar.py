from PyQt5 import QtWidgets

class TabBar(QtWidgets.QTabBar):
    def __init__(self, tab_name: str = None, parent: QtWidgets.QTabWidget = None, *args, **kwargs):
        super(TabBar, self).__init__(parent)
        self._parent = parent
        # self.setTabText(tab_name)


        self._parent.addTab(self, tab_name)
        # self.main_tabwidget.addTab(self.__tab_page, "page 1")