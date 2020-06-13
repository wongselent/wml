from PyQt5 import QtWidgets


class TabBar(QtWidgets.QTabBar):
    def __init__(self, parent: QtWidgets.QTabWidget, tab_title: str = None,
                 tab_widget: QtWidgets.QWidget = None) -> None:
        super(TabBar, self).__init__(parent)
        self.__parent = parent
        self.__tab_title = tab_title
        self.__tab_widget = tab_widget
        self.__tabbar_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

        self.setObjectName(self.__tab_title.replace(" ", "_").lower())
        self.setLayout(self.__tabbar_layout)

        if self.__tab_title:
            self.__parent.addTab(self, self.__tab_title)

        if self.__tab_widget:
            self.__tabbar_layout.addWidget(self.__tab_widget)

        # self.main_tabwidget.addTab(self.__tab_page, "page 1")

    # def append_widget(self, widget: QWidget) -> None:
    #     self.__tabbar_layout.addWidget(widget)

    # if not expand:
    #     vspacer: QSpacerItem = QSpacerItem(0, 1000)
    #     self.__tabbar_layout.addSpacerItem(vspacer)
